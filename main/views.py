from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from .models import User
from products.models import Product,CartItem,Favourites
from modelling.recommendations import recommodation
import requests , os
from django.conf import settings

class User_Register(View):
    def post(self,request):
        email_id = request.POST.get('emailid')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if not all([email_id,password,first_name,last_name]):
            return redirect('/login')
        if User.objects.filter(email=email_id).exists():
            return JsonResponse({'error':'Email ID already exists'},status=404)
        if settings.RECAPTCHA_ENABLED:
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
            'secret': os.environ.get('recaptcha_secret_key'),
            'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                usr = User.objects.create_user(email=email_id,password=password,first_name=first_name,last_name=last_name)
                return render(request,'login_register/login.html')
            else:
                return render(request, 'register.html', {'error': 'Invalid reCAPTCHA. Please try again.'})
        else:
            return render (request,{'status':'Recpatch Done'})
    def get(self,request):
        return render(request,'login_register/register.html')

class User_Login(View):
    def post(self,request):
        email_id = request.POST.get('emailid')
        password = request.POST.get('password')
        if not email_id and password:
            return JsonResponse({'error':'Email or Password is required'})
        user = authenticate(request,username=email_id,password=password)
        if user is None:
            return JsonResponse({'error':'Incorrect Email ID or Password'})
        else:
            login(request,user)
            return redirect ('/')
    def get(self,request):
        return render(request,'login_register/login.html')
        
class Home(View):
    def get(self,request):
        products = Product.objects.order_by('-id')
        recommodation_products = recommodation(request)
        if recommodation_products is None:
                recommodation_products = ""
        print(recommodation_products)
        context = {'user': request.user, 'product': products,'r_product':recommodation_products}
        return render(request, 'index.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


# Create your views here.
