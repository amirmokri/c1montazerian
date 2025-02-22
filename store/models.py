from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to="products/main_images/", null=True, blank=True)
    description = models.TextField(max_length=2000, default="بهترین محصولات را از ما بخواهید.")
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/extra_images/")

    def __str__(self):
        return f"{self.product.name} - {self.id}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.TextField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def update_total_price(self):
        self.total_price = sum(product.price for product in self.products.all())
        self.save()

class Order(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, verbose_name="شماره تلفن")

    def __str__(self):
        return self.user.username