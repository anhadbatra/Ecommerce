import pandas as pd
from products.models import CartItem,Orders

def user_matrix():
    cart_data = pd.DataFrame(list(Orders.objects.all().values('user', 'product_list')))


