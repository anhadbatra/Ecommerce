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
# Create your models here.
