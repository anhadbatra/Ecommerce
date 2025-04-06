from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.Home.as_view()),
    path('register',views.User_Register.as_view(),name='register'),
    path('login',views.User_Login.as_view()),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('allauth.urls')),  # Django Allauth routes

]
