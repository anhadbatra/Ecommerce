from django.db import models
from .storage_backends import MediaStorage


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
    cart_id = models.CharField(primary_key=True,max_length=5)
    total = models.DecimalField(max_digits=9,decimal_places=2)
    quantity = models.IntegerField()
    products = models.JSONField(default=tuple)
    user = models.OneToOneField('main.User', on_delete=models.CASCADE)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    products = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=0)
    user = models.ForeignKey('main.User',on_delete=models.CASCADE)

class Favourites(models.Model):
    products = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey('main.User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'products')

    def __str__(self):
        return f"{self.user.username} - {self.products.name}"



# Create your models here.

class Orders(models.Model):
    order_number = models.IntegerField(unique=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    payment_status = models.IntegerField(default=0)
    payment_date = models.DateTimeField(auto_now=True)
