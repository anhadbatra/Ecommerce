from django.shortcuts import render
from django.views import View
from .models import Product
from django.http import JsonResponse
import boto3
import os

class Products(View):
    def post(self,request):
        try:
            name = request.POST.get('name')
            brand = request.POST.get('brand')
            product_type = request.POST.get('product_type')
            size = request.POST.get('size')
            color = request.POST.get('color')
            price = request.POST.get('price')
            description = request.POST.get('description')
            stock = request.POST.get('stock')
            category = request.POST.get('category')
            material = request.POST.get('material')
            image = request.FILES.get('image')
            try:
                product = Product.objects.create(
                name=name,
                brand=brand,
                product_type=product_type,
                size=size,
                color=color,
                price=price,
                description=description,
                stock=stock,
                category=category,
                material=material
                )
                upload_image = Upload_images_to_s3.upload(name,image)
                if not upload_image:
                    return JsonResponse({'error':'Unable to upload image'})
                product.save()
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    def get(self,request):
        product = Product.objects.all()
        products = {'product':product}
        return render(request,'products/products.html',products)

class Product_Details(View):
    def get(self,request,id):
        product_detail = Product.objects.get(pk=id)
        product_detail_get = {'product_detail': product_detail}
        print(product_detail_get)
        return render(request,'products/product_details.html',product_detail_get)


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
