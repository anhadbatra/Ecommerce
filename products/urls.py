from django.urls import path
from . import views
from modelling.prompts import Result
from visualization.views import ProductVisualisation

urlpatterns = [
    path('products',views.Products.as_view()),
    path('product_detail/<int:id>', views.Product_Details.as_view()),
    path('search_query',Result.as_view()),
    path('add_to_cart',views.Add_to_Cart.as_view()),
    path('view_cart',views.Cart_View.as_view()),
    path('add_to_favourites',views.Favourites_product.as_view()),
    path('order_data',ProductVisualisation.as_view())
]