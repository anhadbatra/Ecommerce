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
    
    
    

 