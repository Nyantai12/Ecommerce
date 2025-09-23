from dbm import sqlite3
import os
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Category, Product  # <- Үүнийг заавал нэмнэ
import sqlite3 as sql

# def index(request):
    # categories = Category.objects.all()  
    # popular_products = Product.objects.all()[:8]  
    # context = {
    #     'categories': categories,
    #     'popular_products': popular_products
    # }
    # return render(request, 'index.html', context)

def index(request):
    categories = Category.objects.raw("SELECT * FROM category")
    popular_products = Product.objects.raw("SELECT * FROM product ORDER BY id DESC LIMIT 8")
    
    context = {
        'categories': categories,
        'popular_products': popular_products
    }
    return render(request, 'index.html', context)




def cart_view(request):
    return render(request, 'cart.html')



def store(request):
    categories = Category.objects.all()  
    popular_products = Product.objects.all()  
    context = {
        'categories': categories,
        'popular_products': popular_products
    }
    return render(request, 'store.html', context)


def signin(request):
    return render(request, 'signin.html')

def register(request):
    return render(request, 'register.html')

def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})

def place_order(request):
    return render(request,'place.html') 
def ordercomp(request):
    return render(request,'order_complete.html') 
def add_to_cart(request, ):
    return render(request, 'cart.html')
def password_reset_view(request):
    return render(request, 'password_reset.html')

def category_products(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {'category': category, 'products': products})