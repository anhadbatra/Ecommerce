from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from .models import User
from products.models import Product

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
        usr = User.objects.create(email=email_id,password=password,first_name=first_name,last_name=last_name)
        usr.save()
        return JsonResponse({'success':'User created successfully'})
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
        products = Product.objects.all()
        product = {'product':products}
        context = {'user': request.user, 'product': product}
        return render(request, 'index.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


# Create your views here.
