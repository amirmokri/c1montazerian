from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Product, Cart, Category, Order, ProductImage
from .serializers import ProductSerializer, CartSerializer, UserSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart = serializer.save(user=self.request.user)
        # ارسال نوتیفیکیشن به ادمین
        print(f"New order by {cart.user.username}: {cart.total_price}")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

from django.shortcuts import render
from .models import Product
import random

def home(request):
    products = list(Product.objects.all())
    random_products = random.sample(products, min(len(products), 3))
    return render(request, 'store/home.html', {'products': random_products})

# صفحه لیست محصولات با جستجو
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
        "categories": categories
    }
    return render(request, "store/products.html", context)

# صفحه مشخصات محصول
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = ProductImage.objects.filter(product=product)
    cart = get_active_cart(request.user) if request.user.is_authenticated else None
    in_cart = cart.products.filter(id=product_id).exists() if cart else False
    return render(request, 'store/product_detail.html', {'product': product, 'images': images, 'in_cart': in_cart})

# صفحه سبد خرید
@login_required(login_url='/login/?next=/cart/')
def cart_view(request):
    cart = get_active_cart(request.user)
    if request.method == 'POST':
        address = request.POST.get('address')
        if not address:
            return JsonResponse({"success": False, "error": "آدرس را وارد کنید!"})
        
        # Create an order
        phone_number = request.user.profile.phone_number
        order = Order.objects.create(user=request.user, address=address, total_price=cart.total_price, phone_number=phone_number)
        order.products.set(cart.products.all())
        cart.products.clear()  # Empty the cart after creating the order
        cart.is_confirmed = True
        cart.save()
        
        return JsonResponse({"success": True, "message": "سفارش شما ثبت شد!"})
    return render(request, 'store/cart.html', {'cart': cart})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

# ورود کاربر با شماره تلفن
def login_view(request):
    next_url = request.GET.get("next", "/")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next", "/")
            return redirect(next_url)
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است!")
    
    context = {
        "next": next_url
    }
    return render(request, "store/login.html", context)

# خروج از حساب
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
        return active_carts.first()
    else:
        return Cart.objects.create(user=user, is_confirmed=False, total_price=0)

@require_POST
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        # Return an error JSON response for visitors who are not logged in.
        return JsonResponse({
            'success': False,
            'error': 'برای افزودن به سبد خرید، لطفا ابتدا وارد حساب کاربری شوید.'
        }, status=403)
    product = get_object_or_404(Product, id=product_id)
    cart = get_active_cart(request.user)
    cart.products.add(product)
    cart.update_total_price()
    return JsonResponse({'success': True, 'total_price': cart.total_price, 'product_id': product_id})

@require_POST
@login_required
def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_active_cart(request.user)
    cart.products.remove(product)
    cart.update_total_price()
    return JsonResponse({'success': True, 'total_price': cart.total_price, 'product_id': product_id})

@csrf_exempt
@require_POST
@login_required
def place_order(request):
    cart = get_active_cart(request.user)

    if not cart or cart.products.count() == 0:
        return JsonResponse({"success": False, "error": "❌ سبد خرید شما خالی است!"})

    address = request.POST.get("address")
    if not address:
        return JsonResponse({"success": False, "error": "⚠️ لطفاً آدرس خود را وارد کنید!"})

    # ایجاد سفارش
    phone_number = request.user.profile.phone_number
    order = Order.objects.create(user=request.user, address=address, total_price=cart.total_price, phone_number=phone_number)
    order.products.set(cart.products.all())

    # پاک کردن سبد خرید پس از ثبت سفارش
    cart.products.clear()
    cart.is_confirmed = True
    cart.save()

    return JsonResponse({"success": True, "message": "✅ سفارش شما با موفقیت ثبت شد! همکاران ما در اسرع وقت برای تأیید نهایی و هماهنگی ارسال با شما تماس خواهند گرفت. از اعتماد شما متشکریم! 🙏"})