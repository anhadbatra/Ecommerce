import pandas as pd
from products.models import CartItem,Orders,Favourites

def user_matrix():
    order_data = pd.DataFrame(list(Orders.objects.all().values('user', 'product_list')))
    favourites = pd.DataFrame(list(Favourites.objects.all().values('products','user')))
    cart_items = pd.DataFrame(list(CartItem.objects.all().values('products','user')))
    # give preferences 
    cart_items_preference = 2
    order_data_preference = 3
    favourites_preference = 1
    


