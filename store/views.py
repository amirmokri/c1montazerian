from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Product, Cart, Category, Order, ProductImage, UserProfile
from .serializers import ProductSerializer, CartSerializer, UserSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import random

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart = serializer.save(user=self.request.user)
        # Send notification to admin
        print(f"New order by {cart.user.username}: {cart.total_price}")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def home(request):
    products = list(Product.objects.all())
    random_products = random.sample(products, min(len(products), 3))
    return render(request, 'store/home.html', {'products': random_products})

def product_list(request):
    query = request.GET.get("q", "")
    category_id = request.GET.get("category", "")

    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    
    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        "products": products,
        "categories": categories,
        "query": query,
        "category_id": int(category_id) if category_id else None
    }
    return render(request, "store/products.html", context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = ProductImage.objects.filter(product=product)
    cart = get_active_cart(request.user) if request.user.is_authenticated else None
    in_cart = cart.products.filter(id=product_id).exists() if cart else False
    return render(request, 'store/product_detail.html', {'product': product, 'images': images, 'in_cart': in_cart})

@login_required(login_url='/login/?next=/cart/')
def cart_view(request):
    cart = get_active_cart(request.user)
    message = None
    error = None

    if request.method == 'POST':
        address = request.POST.get('address')

        if not address:
            error = "⚠️ لطفاً آدرس خود را وارد کنید!"
        elif cart.products.count() == 0:
            error = "❌ سبد خرید شما خالی است!"
        else:
            phone_number = request.user.profile.phone_number
            if not phone_number:
                error = "⚠️ لطفاً شماره تلفن خود را در پروفایل کاربری وارد کنید!"
            else:
                order = Order.objects.create(
                    user=request.user,
                    address=address,
                    total_price=cart.total_price,
                    phone_number=phone_number
                )
                order.products.set(cart.products.all())

                cart.products.clear()
                cart.is_confirmed = True
                cart.save()

                message = "✅ سفارش شما با موفقیت ثبت شد! همکاران ما در اسرع وقت برای تأیید نهایی و هماهنگی ارسال با شما تماس خواهند گرفت."

    return render(request, 'store/cart.html', {'cart': cart, 'message': message, 'error': error})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user, phone_number=form.cleaned_data["phone_number"])

            login(request, user)
            messages.success(request, "🎉 به باشگاه مشتریان خوش آمدید! امیدواریم با ارائه بهترین خدمات، اعتماد شما را جلب کنیم.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "store/register.html", {"form": form})

def login_view(request):
    next_url = request.GET.get("next", "/")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get("next", "/")
                return redirect(next_url)
            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است!")
        else:
            messages.error(request, "لطفاً فرم را به درستی پر کنید.")
    else:
        form = LoginForm()

    context = {
        "form": form,
        "next": next_url
    }
    return render(request, "store/login.html", context)

def logout_view(request):
    logout(request)
    return redirect('home')

def get_active_cart(user):
    active_carts = Cart.objects.filter(user=user, is_confirmed=False)
    if active_carts.count() > 1:
        # Consolidate duplicated active carts.
        cart = active_carts.first()
        for duplicate in active_carts.exclude(id=cart.id):
            # Add any missing products from duplicates.
            for product in duplicate.products.all():
                cart.products.add(product)
            duplicate.delete()
        # Update total price.
        cart.update_total_price()
        return cart
    elif active_carts.exists():
        cart = active_carts.first()
        cart.update_total_price()  # Ensure the total price is updated
        return cart
    else:
        return Cart.objects.create(user=user, is_confirmed=False, total_price=0)

@require_POST
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": False, "error": "برای افزودن به سبد خرید، لطفاً ابتدا وارد حساب کاربری شوید."}, status=403)
        else:
            messages.error(request, "برای افزودن به سبد خرید، لطفاً ابتدا وارد حساب کاربری شوید.")
            return redirect("login")

    product = get_object_or_404(Product, id=product_id)
    cart = get_active_cart(request.user)
    cart.products.add(product)
    cart.update_total_price()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context = {
            "product": product,
            "cart": cart,
            "message": f"✅ {product.name} به سبد خرید اضافه شد!"
        }
        return render(request, "store/partials/cart_update.html", context)
    else:
        messages.success(request, f"✅ {product.name} به سبد خرید اضافه شد!")
        return redirect("cart_view")


@login_required
@require_POST
def remove_product(request, product_id):
    cart = get_active_cart(request.user)
    product = get_object_or_404(Product, id=product_id)
    
    if product in cart.products.all():
        cart.products.remove(product)
        cart.update_total_price()  # Update the total price
        cart.save()  # Save the cart
        return JsonResponse({
            "success": True,
            "total_price": cart.total_price
        })
    else:
        return JsonResponse({
            "success": False,
            "error": "محصول مورد نظر در سبد خرید شما وجود ندارد."
        })

@csrf_exempt
@login_required
@require_POST
def place_order(request):
    cart = get_active_cart(request.user)

    if not cart.products.exists():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                "success": False,
                "error": "🚨 سبد خرید شما خالی است! لطفاً ابتدا محصولی اضافه کنید."
            })
        else:
            messages.error(request, "🚨 سبد خرید شما خالی است! لطفاً ابتدا محصولی اضافه کنید.")
            return redirect("cart_view")

    address = request.POST.get("address")
    if not address:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                "success": False,
                "error": "📍 لطفاً آدرس خود را وارد کنید!"
            })
        else:
            messages.error(request, "📍 لطفاً آدرس خود را وارد کنید!")
            return redirect("cart_view")

    # Create the order
    order = Order.objects.create(
        user=request.user,
        address=address,
        total_price=cart.total_price,
        phone_number=request.user.profile.phone_number
    )
    order.products.set(cart.products.all())

    # Clear the cart
    cart.products.clear()
    cart.is_confirmed = True
    cart.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            "success": True,
            "message": "✅ سفارش شما با موفقیت ثبت شد! همکاران ما برای هماهنگی ارسال با شما تماس خواهند گرفت."
        })
    else:
        messages.success(request, "✅ سفارش شما با موفقیت ثبت شد! همکاران ما برای هماهنگی ارسال با شما تماس خواهند گرفت.")
        return redirect("cart_view")