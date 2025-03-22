import pandas as pd
from products.models import CartItem,Orders,Favourites,Product
from django.views import View
from sklearn.metrics.pairwise import cosine_similarity



def recommodation(request):
        order_data = pd.DataFrame(list(CartItem.objects.all().values('user', 'products')))
        favourites = pd.DataFrame(list(Favourites.objects.all().values('products', 'user')))
        order_data['products'] = order_data['products'].apply(lambda x : list(x.keys()))
        order_data['weight'] = 1
        favourites['weight'] = 2  
        order_data = order_data.explode('products').rename(columns={'products': 'product'}) # expand list like columns into single column
        favourites = favourites.explode('products').rename(columns={'products': 'product'})
        combined_data = pd.concat([order_data[['user', 'product', 'weight']],  # concatinating into one dataframe
                              favourites[['user', 'product', 'weight']]])
        
        user_item_matrix = combined_data.pivot_table(index='user', columns='product', 
                                                    values='weight', aggfunc='sum', fill_value=0)

        # Compute similarity between users
        user_similarity = cosine_similarity(user_item_matrix)
        user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, 
                                        columns=user_item_matrix.index)
        print(user_similarity_df.head())

        # Example: Recommend products for a specific user (e.g., user_id=1)
        user_id = request.user.id
        print(user_id)
        if user_id is None:
                return
        if user_id not in user_item_matrix.index:
                return []
        
        similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:]  # Exclude self
        similar_users_products = user_item_matrix.loc[similar_users.index].mean(axis=0)
        recommendations = similar_users_products.sort_values(ascending=False).head(5)

        print(f"Recommendations for user {user_id}:")
        print(recommendations)
        product_ids = recommendations.index.tolist()
        matching_products = Product.objects.filter(pk__in=product_ids)
        return matching_products
        
        

    