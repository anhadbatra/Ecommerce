from django.urls import path
from . import views
from modelling.prompts import Result

urlpatterns = [
    path('products',views.Products.as_view()),
    path('product_detail/<int:id>', views.Product_Details.as_view()),
    path('search_query',Result.as_view())
    

]