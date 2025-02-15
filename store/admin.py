from django.contrib import admin
from .models import Product, Cart, UserProfile, Category, Order, ProductImage
from django.contrib.auth.models import User

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(ProductImage)