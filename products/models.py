from django.db import models
from .storage_backends import MediaStorage

Color_choices =(
    ('black','BLACK'),
    ('white','WHITE'),
    ('blue','BLUE'),
    ('red','RED'),
    ('orange','ORANGE'),
)
Categories = (
    ('loafers','Loafers'),
    ('sports shoes','Sport Shoes'),
    ('Sneakers','Sneakers'),
    ('Platform Shoe','Platform Shoe')
)
Brand = (
    ('Adidas','Adidas'),
    ('Nike','Nike'),
    ('New Balance','New Balance'),
    ('Skechers','Skechers'),

)


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=20,choices=Brand,default='Adidas')
    size = models.IntegerField() 
    color = models.CharField(max_length=10,choices=Color_choices,default='black')  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    category = models.CharField(max_length=15,choices=Categories,default='Loafers')
    image_main = models.FileField(storage=MediaStorage())

    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    products = models.JSONField(default=dict)
    user = models.ForeignKey('main.User',on_delete=models.CASCADE)

class Cart(models.Model):
    cart_id = models.ForeignKey(CartItem,on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9,decimal_places=2)
    quantity = models.IntegerField()
    products = models.JSONField(default=tuple)
    user = models.OneToOneField('main.User', on_delete=models.CASCADE)

class Favourites(models.Model):
    products = models.JSONField(default=list)
    user = models.ForeignKey('main.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.products}"



# Create your models here.

class Orders(models.Model):
    user = models.ForeignKey('main.User', on_delete=models.CASCADE)
    order_number = models.IntegerField(unique=True)
    products = models.JSONField(default=list)
    payment_status = models.IntegerField(default=0)
    payment_date = models.DateTimeField(auto_now=True)  
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    stripe_payment_intent = models.CharField(max_length=255, null=True)
    stripe_customer_id = models.CharField(max_length=255, null=True)
    stripe_session_id = models.CharField(max_length=255, null=True)
    payment_status = models.CharField(max_length=50, null=True)
    receipt_email = models.EmailField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

