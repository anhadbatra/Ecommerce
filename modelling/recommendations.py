import pandas as pd
from products.models import CartItem,Orders,Favourites
from django.views import View


class Test(View):
    def get(self,request):
        order_data = pd.DataFrame(list(CartItem.objects.all().values('user', 'products')))
        favourites = pd.DataFrame(list(Favourites.objects.all().values('products', 'user')))
        order_data['products'] = order_data['products'].apply(lambda x : list(x.keys()))
        order_data['weight'] = 1
        favourites['weight'] = 2  
        order_data = order_data.explode('products').rename(columns={'products': 'product'}) # expand list like columns into single column
        favourites = favourites.explode('products').rename(columns={'products': 'product'})
        combined_data = pd.concat([order_data[['user', 'product', 'weight']],  # concatinating into one dataframe
                              favourites[['user', 'product', 'weight']]])
        
        print(combined_data)
        
        

    