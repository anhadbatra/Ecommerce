import pandas as pd
from products.models import CartItem,Orders,Favourites,Product
from django.views import View
from sklearn.metrics.pairwise import cosine_similarity

def safe_explode(df, col):
    if col in df.columns:
        df[col] = df[col].apply(lambda x: x if isinstance(x, list) else [])
        df = df.explode(col)
        df = df.rename(columns={col: 'product'})
    else:
        df['product'] = None  # fallback
    return df

def ensure_list(x):
    if isinstance(x, list):
        return x
    return []



def recommodation(request):
        order_data = pd.DataFrame(list(Orders.objects.all().values('user', 'products')))
        favourites = pd.DataFrame(list(Favourites.objects.all().values('products', 'user')))
        print(list(Favourites.objects.values('products', 'user'))[:2])

        if 'products' in order_data.columns:
                order_data['products'] = order_data['products'].apply(ensure_list)
        else:
                order_data['products'] = []

        if 'products' in favourites.columns:
                favourites['products'] = favourites['products'].apply(ensure_list)
        else:
                favourites['products'] = []

        order_data['weight'] = 1
        favourites['weight'] = 2

        order_data = safe_explode(order_data, 'products')
        favourites = safe_explode(favourites, 'products')


        order_data['product'] = order_data['product'].apply(lambda x: int(x) if pd.notna(x) else None)
        favourites['product'] = favourites['product'].apply(lambda x: int(x) if pd.notna(x) else None)

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
        print(combined_data.head())
        if order_data.empty and favourites.empty:
                return Product.objects.none()
        
        user_item_matrix = combined_data.pivot_table(index='user', columns='product', 
                                                    values='weight', aggfunc='sum', fill_value=0)
        print(user_item_matrix)
        if user_item_matrix.empty or user_item_matrix.shape[0] < 2:
    # Fallback: return top 5 most ordered products overall
                top_products = (
                combined_data['product'].value_counts().head(5).index.tolist()
    )
                product_ids = [int(float(pid)) for pid in top_products if pd.notna(pid)]
                return Product.objects.filter(pk__in=product_ids)
        user_similarity = cosine_similarity(user_item_matrix)
        user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, 
                                        columns=user_item_matrix.index)
        print(user_similarity_df.head())

        # Example: Recommend products for a specific user (e.g., user_id=1)
        user_id = request.user.id
        if user_id is None:
               return []
        
        try:
                similar_users = user_similarity_df.loc[user_id].sort_values(ascending=False)[1:]  # exclude self
        except KeyError:
                similar_users = pd.Series()
        similar_users_products = user_item_matrix.loc[similar_users.index].mean(axis=0)
        recommendations = similar_users_products.sort_values(ascending=False)

        print(f"Recommendations for user {user_id}:")
        print(recommendations)
        product_scores = recommendations.to_dict()

# Convert to int, filter out None
        product_ids = [int(float(pid)) for pid in product_scores.keys() if pd.notna(pid)]

        print("Product IDs to fetch:", product_ids)
        print("Available DB Product IDs:", list(Product.objects.values_list('id', flat=True)))

        products = list(Product.objects.filter(pk__in=product_ids))

# Sort back by recommendation weight
        products_sorted = sorted(products, key=lambda p: product_scores.get(p.pk, 0), reverse=True)

        return products_sorted
        
        

    