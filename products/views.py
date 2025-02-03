from django.shortcuts import render
from django.views import View
from main import models
from django.http import JsonResponse
import boto3

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
            try:
                product = Products.objects.create(
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
                Upload_images_to_s3.post(name)
                product.save()
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

class Upload_images_to_s3():
    def post(self,name):




# Create your views here.
