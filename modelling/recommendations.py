import pandas as pd
from products.models import CartItem,Orders,Favourites,Product
from django.views import View
from sklearn.metrics.pairwise import cosine_similarity

def safe_explode(df, col):
    if col in df.columns and not df[col].isnull().all():
        df[col] = df[col].apply(lambda x: list(x) if pd.notnull(x) else [])
        df = df.explode(col)
        df = df.rename(columns={col: 'product'})
    else:
        df['product'] = None  # fallback
    return df

def recommodation(request):
        order_data = pd.DataFrame(list(Orders.objects.all().values('user', 'products')))
        favourites = pd.DataFrame(list(Favourites.objects.all().values('products', 'user')))
        if 'products' in order_data.columns and not order_data['products'].isnull().all():
            order_data['products'] = order_data['products'].apply(lambda x: list(x) if pd.notnull(x) else [])
        else:
            order_data['products'] = []
        if 'products' in favourites.columns and not favourites['products'].isnull().all():
              favourites['products'] = favourites['products'].apply(lambda x: list(x) if pd.notnull(x) else [])
        else:
              favourites['products'] = []
        order_data['weight'] = 1
        favourites['weight'] = 2  
        order_data = safe_explode(order_data, 'products')
        favourites = safe_explode(favourites, 'products')
        order_data['product'] = order_data['product'].apply(lambda x: x.get('product_id') if isinstance(x, dict) else x)
        favourites['product'] = favourites['product'].apply(lambda x: x.get('product_id') if isinstance(x, dict) else x)
        required_cols = ['user', 'product', 'weight']
        for col in required_cols:
                if col not in order_data.columns:
                        order_data[col] = None
                if col not in favourites.columns:
                        favourites[col] = None

        combined_data = pd.concat([
        order_data[required_cols],
        favourites[required_cols]
        ])
        if order_data.empty and favourites.empty:
                return Product.objects.none()
        
        user_item_matrix = combined_data.pivot_table(index='user', columns='product', 
                                                    values='weight', aggfunc='sum', fill_value=0)
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
        
        

    