from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home.as_view()),
    path('register',views.User_Register.as_view()),
    path('login',views.User_Login.as_view()),
    

]
