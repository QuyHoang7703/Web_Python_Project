from django.shortcuts import render
from .models import *
from django.core.exceptions import ObjectDoesNotExist
def home(request):
    products = Product.objects.all()
    return render(request,'home.html', {'products': products})

def filter_product(request,brand_id):
    products = Product.objects.filter(category__name_category=brand_id)
    return render(request,'filter_product.html', {'products': products})


def search_product(request):
    query = request.GET.get('q')
    if query:
        product_names = Product.objects.filter(name__icontains=query)           
    else:
        product_names = Product.objects.all()
    return render(request, 'search_product.html', {'product_names': product_names}) 



