from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CartViewSet, UserViewSet
from .views import home, product_list, product_detail, cart_view, login_view, register_view, logout_view, add_to_cart, remove_product

# تنظیم روت‌های API
router = DefaultRouter()
router.register('api/insertproducts', ProductViewSet)  # مسیر API برای محصولات
router.register('api/carts', CartViewSet)  # مسیر API برای سبد خرید
router.register('api/users', UserViewSet)  # مسیر API برای کاربران

urlpatterns = [
    # مسیرهای مربوط به API
    path('', include(router.urls)),  # حالا API فقط روی /api نمایش داده میشه

    # مسیرهای مربوط به قالب‌های HTML
    path('home/', home, name='home'),  # صفحه اصلی
    path('products/', product_list, name='products'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'), 
    path('remove-product/<int:product_id>/', remove_product, name='remove_product'), # صفحه لیست محصولات
    path('product_detail/<int:product_id>/', product_detail, name='product_detail'),  # صفحه هر محصول
    path('cart/', cart_view, name='cart'),  # صفحه سبد خرید
    path('register/', register_view, name='register'),  # صفحه ثبت‌نام
    path('login/', login_view, name='login'),  # صفحه ورود
    path('logout/', logout_view, name='logout'),  # صفحه خروج
]