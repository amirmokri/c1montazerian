from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CartViewSet, UserViewSet,
    home, product_list, product_detail,
    cart_view, login_view, register_view,
    logout_view, add_to_cart, remove_product, place_order
)



urlpatterns = [
    # مسیرهای اصلی (HTML Templates)
    path('', home, name='home'),  # صفحه اصلی
    path('products/', product_list, name='products'),  # لیست محصولات
    path('product/<int:product_id>/', product_detail, name='product_detail'),  # صفحه جزئیات محصول
    path('cart/', cart_view, name='cart_view'),  # صفحه سبد خرید
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),  # افزودن محصول به سبد خرید
    path('cart/remove/<int:product_id>/', remove_product, name='remove_product'),  # حذف محصول از سبد خرید
    path('place_order/', place_order, name='place_order'),  # ثبت سفارش
    
    # مسیرهای احراز هویت
    path('register/', register_view, name='register'),  # صفحه ثبت‌نام
    path('login/', login_view, name='login'),  # صفحه ورود
    path('logout/', logout_view, name='logout'),  # خروج از حساب

]
