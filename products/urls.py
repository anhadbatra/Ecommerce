from django.urls import path
from . import views
from modelling.prompts import Result
from .views import CheckoutSession, MyOrdersView, Order_details_view, PaymentSuccess, PaymentCancel, remove_from_cart_view
from visualization.views import ProductVisualisation
from .views import CheckoutSession, OrderDetailsView, PaymentSuccess, PaymentCancel

urlpatterns = [
    path('products',views.Products.as_view()),
    path('product_detail/<int:id>', views.Product_Details.as_view()),
    path('search_query',Result.as_view()),
    path('add_to_cart',views.Add_to_Cart.as_view()),
    path('remove-from-cart/', remove_from_cart_view.as_view(), name='remove-from-cart'),
    path('view_cart',views.Cart_View.as_view()),
    path('add_to_favourites',views.Favourites_product.as_view()),
    # payment paths 
    path('create-checkout-session/', CheckoutSession.as_view(), name='create-checkout-session'),
    path('payment-success/', PaymentSuccess.as_view(), name='payment-success'),
    path('payment-cancel/', PaymentCancel.as_view(), name='payment-cancel'),
    path('order/<int:order_number>/', Order_details_view.as_view(), name='order-details'),
    path('my-orders/', MyOrdersView.as_view(), name='my-orders'),
    path('add_to_favourites',views.Favourites_product.as_view()),
    path('order_data',ProductVisualisation.as_view())
]