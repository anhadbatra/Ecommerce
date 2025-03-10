from django.contrib import admin
from .models import Product,CartItem,Favourites

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Favourites)
# Register your models here.
