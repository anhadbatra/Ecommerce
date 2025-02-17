from django.db import models
from .storage_backends import MediaStorage
from  main.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=20)
    product_type = models.CharField(max_length=100)
    size = models.IntegerField() 
    color = models.CharField(max_length=20)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    category = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    image_main = models.FileField(storage=MediaStorage())

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    cart_id = models.CharField(primary_key=True)
    total = models.DecimalField(max_digits=9,decimal_places=2)
    quantity = models.IntegerField()
    user = models.OneToOneField(User)
    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    products = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=0)
    user = models.OneToOneField(User)


# Create your models here.
