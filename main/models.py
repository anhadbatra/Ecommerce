from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import CustomUserModel
from django.utils import timezone
from products.models import Product

class User(AbstractBaseUser,PermissionsMixin):
        email = models.EmailField(unique=True)
        first_name = models.CharField(max_length=30, blank=True)
        last_name = models.CharField(max_length=30, blank=True)
        date_joined = models.DateTimeField(default=timezone.now)
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False)
        preferences = models.JSONField(default=dict, blank=True)  # Example: preferred sizes, brands
        payment_methods = models.JSONField(default=list, blank=True)  # Example: saved card details

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []

        objects = CustomUserModel()

        def __str__(self):
            return self.email
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]
    PAYMENT_STATUS_CHOICES = [
    ('Paid', 'Paid'),
    ('Unpaid', 'Unpaid'),
    ] 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Unpaid')
    payment_method = models.CharField(max_length=50)
    shipping_address = models.JSONField()
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "f Order{self.id} placed by {self.user.username}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_purchase = models.BooleanField(default=False)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"
    

