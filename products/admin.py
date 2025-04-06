from django.contrib import admin
from .models import Product,CartItem,Favourites,Orders

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Favourites)
admin.site.register(Orders)
# Register your models here.
