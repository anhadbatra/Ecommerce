from django.shortcuts import render
from django.views import View


class Products(View):
    def post(self,request):
        return 'Hello'
# Create your views here.
