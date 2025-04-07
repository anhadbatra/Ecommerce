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
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

stripe.api_key =os.environ.get('STRIPE_SECRET_KEY') 
class Products(View):
    def post(request):
        color = request.POST.get('color')
        category = request.POST.get('category')
        if color:
            product = Product.objects.get(color=color)
        if category:
            product = Product.objects.get(category=category)
        product_details = {'product_filter':product}
        return render(request,'products/product_details.html',product_details)

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
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))
        get_user = request.user

        try:
            cart_item, created = CartItem.objects.get_or_create(
                user=get_user,
                defaults={'products': {product_id: 1}}
            )

            if not created:
                current_products = cart_item.products or {}
                current_products[product_id] = current_products.get(product_id, 0) + 1
                cart_item.products = current_products
                cart_item.save()

            product = Product.objects.get(pk=product_id)

            return JsonResponse({
                'status': 'success',
                'message': f"{product.name} added to cart",
                'cart_count': sum(cart_item.products.values())  # optional
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    



class Cart_View(View):
    def get(self, request):
        get_user = request.user
        cart_items = CartItem.objects.filter(user=get_user)

        cart_data = {}
        total_price = 0

        for cart_item in cart_items:
            product_data = cart_item.products
            for product_id, quantity in product_data.items():
                cart_data[int(product_id)] = cart_data.get(int(product_id), 0) + quantity

        if not cart_data:
            return render(request, 'products/view_cart.html', {'cart_items': {}, 'error': 'Your cart is empty.'})

        product_objects = Product.objects.filter(id__in=cart_data.keys())
        cart_with_details = {}

        for product in product_objects:
            item_total_price = product.price * cart_data[product.id]
            total_price += item_total_price
            cart_with_details[product.id] = {
                'id': product.id,
                'image': f"{settings.MEDIA_URL}{product.image_main}",
                'name': product.name,
                'quantity': cart_data[product.id],
                'price': product.price,
                'total_price': item_total_price
            }

        return render(request, 'products/view_cart.html', {
            'cart_items': cart_with_details,
            'total_price': total_price,
            'STRIPE_PUBLISHABLE_KEY': os.environ.get('STRIPE_PUBLISHABLE_KEY')
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
                'status':'removed',
                'message': "Product removed from Favourite"
            })
        else:
            favourite.products.append(product_id) # else it will append into new
            favourite.save()
            return JsonResponse({
                'status':'added',
                'message': "Product added to Favourite"
            })
class CheckoutSession(View):
    def post(self, request):
        user = request.user
        try:
            cart_item = CartItem.objects.get(user=user)
            line_items = []
            for product_id, quantity in cart_item.products.items():
                product = Product.objects.get(id=product_id)
                print(product)
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

            last_order = Orders.objects.order_by('-timestamp').first()
            order_number = order_number_generation(last_order.order_number if last_order else None)

            order_items = []
            products = []
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
                products.append(product_id)

            # Save order
            order = Orders.objects.create(
                user=request.user,
                order_number=order_number,
                products=products,
                total_amount=total_amount,
                stripe_payment_intent=session.payment_intent,
                stripe_customer_id=session.customer,
                stripe_session_id=session.id,
                payment_status=session.payment_status,
                receipt_email=session.customer_email
            )

            # Clear cart
            cart_item.delete()

            email_body = render_to_string('products/order_success_email_template.html', {
                'user': user,
                'order': order,
                'products': order_items,
            })

            send_mail(
                subject=f"Order Confirmation - #{order.order_number}",
                message="Thanks for your order!",
                from_email="artperformtogether@gmail.com",
                recipient_list=[request.user.email],
                html_message=email_body
            )

            messages.success(request, "Order Placed Successfully!")

            return render(request, 'products/order_details.html', {
                'order': order,
                'products': order_items
            })

        except Exception as e:
            return render(request, 'payment_success.html', {'message': f"Error: {str(e)}"})

class PaymentCancel(View):
    def get(self, request):
        return render(request, 'payment_cancel.html', {'message': 'Payment was cancelled. You can try again.'})


def order_number_generation(order_number):
    return order_number + 1 if order_number else 1000

class Order_details_view(View):
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


class remove_from_cart_view(View):
    def post(self, request):
        user = request.user
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))  # keys are stored as str in JSONField

        try:
            cart_item = CartItem.objects.get(user=user)
            if product_id in cart_item.products:
                del cart_item.products[product_id]
                cart_item.save()
                msg ="Product removed successfully"
                messages.success(request,msg)
                return JsonResponse({'status': 'removed',"messages":msg})
            else:
                return JsonResponse({'status': 'not found'}, status=404)
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'cart not found'}, status=404)
class MyOrdersView(View):
    def get(self, request):
        user = request.user
        orders = Orders.objects.filter(receipt_email=user.email).order_by('-timestamp')

        return render(request, 'products/my_orders.html', {'orders': orders})
# Create your views here.


