from django.shortcuts import render
from django.views import View
from .models import Product , Favourites , Cart , Orders
from django.http import JsonResponse
import boto3
import os
from django.conf import settings
import json
from django.http import JsonResponse
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class Products(View):
    def post(request):
        price_range = request.POST.get('range')
        color = request.POST.get('color')
        category = request.POST.get('category')
        if price_range:
            Product.objects.get()
        if color:
            product = Product.objects.get(color=color)
        if category:
            product = Product.objects.get()

    def get(self,request):
        product = Product.objects.all()
        products = {'product':product}
        return render(request,'products/products.html',products)

class Product_Details(View):
    def get(request,id):
        product_detail = Product.objects.get(pk=id)
        product_detail_get = {'product_detail': product_detail}
        return render(request,'products/product_details.html',product_detail_get)

class Add_to_Cart(View):
    def post(self, request):
        data = json.loads(request.body)
        product_id_from_body = data.get('product_id')
        get_user = request.session.get('user')
        

        
class Cart_Checkout(View):
    def post(request):
        product_list = request.POST.get('product_list')
        total_amount = request.POST.get('amount')
        quantity = request.POST.get('quantity')
        user = request.session.get('user')
        Cart_Store = Cart.objects.create(product_list=product_list,total_amount=total_amount,quantity=quantity,user=user)
        Cart_Store.save()
        return render(request,'products/checkout.html')

    def get(request):
        user = request.session.get('user')
        cart_details = Cart.objects.get(user=user)
        cart_details_get = {'cart_details'}



class Upload_images_to_s3():
    @staticmethod
    def post(name,image):
        s3,bucket_name = connect_S3()
        try:
            file_name = "f{name}/{image}"
            s3.upload_fileobj(
                image,
                bucket_name,
                file_name
            )
            return JsonResponse ({'success':'File uploaded successfully'})
        except Exception as e:
            return JsonResponse ({'error':'uploading image'})

class Favourites(View):
    def post(request,id):
        result = Product.objects.get(id=id)
        favorite, created = Favourites.objects.get_or_create(user=request.user, products=result)
        if not created:
            favorite.delete()
        
class CheckoutSession(View):
    def post(*args,**kwargs):
        cart = Cart.objects.get(id=id)
        checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(cart.price) * 100,
                        "product_data": {
                            "name": cart.pro
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )

    def payment_sucess(request):
        if 'success' in request.GET:
            last_order = Orders.objects.latest('timestamp')
            order_number = last_order.order_number
            order_number = order_number_generation(order_number)
            create_order = Orders.objects.create(
                order_number= order_number,

            )

    

def order_number_generation(order_number):
    if order_number is not None:
        order_number += 1
        return order_number
    else:
        order_number = 1000
        return order_number

        


            
def connect_S3():
    BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    s3 = boto3.client(
        's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
    return s3 , BUCKET_NAME



# Create your views here.
