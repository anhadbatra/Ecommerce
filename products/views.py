from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import  Product , Favourites , Cart , Orders , CartItem
from django.http import JsonResponse
import boto3
import os
from django.conf import settings
import json
from django.http import JsonResponse
import stripe

stripe.api_key = "sk_test_51QwDJ2BHn3y4UQlTWT0wZ25ObGSBYkBft8GsfEO3eJnUD9xJRzxruAuf6sGJVrV82LUq5VT88nPLnp2sTQKvicfg00WDP5d7v3"#settings.STRIPE_SECRET_KEY
print("Raw key:-"   , repr(stripe.api_key))   # Shows hidden characters if any
print("Starts with sk_test_:", stripe.api_key.startswith("sk_test_"))
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
    def get(self,request,id):
        product_detail = Product.objects.get(pk=id)
        product_detail_get = {'product_detail': product_detail}
        return render(request,'products/product_details.html',product_detail_get)

class Add_to_Cart(View):
    def post(self, request):
        products = []
        data = json.loads(request.body)
        product_id = data.get('product_id')
        get_user = request.user
        cart_item, created = CartItem.objects.get_or_create(
                user=get_user,
                defaults={'products':{product_id:1}}  # Store product_id in a list/tuple
            )
        if not created:
                current_products = cart_item.products
                current_products[product_id] = current_products.get(product_id, 0) + 1
                cart_item.products = current_products
                cart_item.save()
        print(json.dumps(cart_item.products))
        product_detail = Product.objects.get(pk=product_id)
        product_detail_get = {'product_detail': product_detail}
        return render(request,'products/product_details.html',product_detail_get)

class Cart_View(View):
    def get(self, request):
        get_user = request.user
        cart_items = CartItem.objects.filter(user=get_user)
        cart_data = {}
        total_price = 0  # initialize total cart price
        for cart_item in cart_items:
            product_data = cart_item.products 
            for product_id, quantity in product_data.items():
                cart_data[int(product_id)] = cart_data.get(int(product_id), 0) + quantity 
        if not cart_data:
            return render(request, 'products/view_cart.html', {'cart_items': {}, 'error': 'Your cart is empty.'})
        # get product details from DB
        product_objects = Product.objects.filter(id__in=cart_data.keys())
        print(product_objects)
        for product in product_objects:
            item_total_price = product.price * cart_data[product.id] #count of product items into product price  
            total_price += item_total_price  
            cart_with_details = {}
            cart_with_details[product.id] = {
                'id': product.id,
                'image': f"{settings.MEDIA_URL}{product.image_main}", 
                'name': product.name,
                'quantity': cart_data[product.id],
                'price': product.price, 
                'total_price': item_total_price
            }
        return render(request, 'products/view_cart.html', 
            {
            'cart_items': cart_with_details,
            'total_price': total_price,
            'STRIPE_PUBLISHABLE_KEY':os.environ.get('STRIPE_PUBLISHABLE_KEY')
            })
        
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

class Favourites_product(View):
    def post(self,request):
        user = request.user
        data = json.loads(request.body)
        product_id = data.get('product_id')
        favourite, added = Favourites.objects.get_or_create(
                user=user,
                defaults={'products': []}
        )
        if product_id in favourite.products: # if the product id is already present
            favourite.products.remove(product_id)
            favourite.save()
            return JsonResponse({
                'status':'removed'
            })
        else:
            favourite.products.append(product_id) # else it will append into new
            favourite.save()
            return JsonResponse({
                'status':'added'
            })

            
        

        
class CheckoutSession(View):
    def post(self, request):
        user = request.user
        try:
            cart_item = CartItem.objects.get(user=user)
            line_items = []

            for product_id, quantity in cart_item.products.items():
                product = Product.objects.get(id=product_id)
                line_items.append({
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(product.price * 100),  # Price in cents
                        "product_data": {
                            "name": product.name,
                        },
                    },
                    "quantity": quantity,
                })

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url="http://127.0.0.1:8000/payment-success/" + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://127.0.0.1:8000/payment-cancle/",
                customer_email=user.email,
            )
            print(checkout_session)
            return JsonResponse({'id': checkout_session.id})

        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'No cart found for this user'}, status=404)
class PaymentSuccess(View):
    def get(self, request):
        user = request.user
        session_id = request.GET.get('session_id')

        if not session_id:
            return render(request, 'payment_success.html', {'message': 'No session ID found.'})

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)

            cart_item = CartItem.objects.get(user=user)

            # Generate new order number
            last_order = Orders.objects.order_by('-timestamp').first()
            order_number = order_number_generation(last_order.order_number if last_order else None)

            order_items = []
            total_amount = 0

            for product_id, quantity in cart_item.products.items():
                product = Product.objects.get(id=product_id)
                total_price = float(product.price) * quantity
                total_amount += total_price

                order_items.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'price': float(product.price),
                    'quantity': quantity,
                    'total_price': total_price
                })

            # Save order
            Orders.objects.create(
                order_number=order_number,
                products=order_items,
                total_amount=total_amount,
                stripe_payment_intent=session.payment_intent,
                stripe_customer_id=session.customer,
                stripe_session_id=session.id,
                payment_status=session.payment_status,
                receipt_email=session.customer_email
            )
            # Clear cart
            cart_item.delete()
            context = {
                'order': order_number,
                'products': order_items,  # JSON list
            }
            return render(request, 'products/order_details.html', context)

        except Exception as e:
            return render(request, 'payment_success.html', {'message': f"Error: {str(e)}"})

class PaymentCancel(View):
    def get(self, request):
        return render(request, 'payment_cancel.html', {'message': 'Payment was cancelled. You can try again.'})


def order_number_generation(order_number):
    return order_number + 1 if order_number else 1000

class OrderDetailsView(View):
    def get(self, request, order_number):
        order = get_object_or_404(Orders, order_number=order_number, receipt_email=request.user.email)
        context = {
            'order': order,
            'products': order.products,  # JSON list
        }
        return render(request, 'products/order_details.html', context)
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


