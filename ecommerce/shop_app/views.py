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
    paginator = Paginator(popular_products, 4)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    context = {
        'categories': categories,
        'popular_products': products ,
    }
    return render(request, 'store.html', context)







def category_products(request, slug):
    categories = Category.objects.all()
    category = get_object_or_404(Category, slug=slug)
    popular_products = Product.objects.filter(category=category)
    return render(request, 'store.html', {
        'categories': categories,
        'popular_products': popular_products,
        'selected_category': category
    })  



def signin(request):
    return render(request, 'signin.html')

def register(request):
    return render(request, 'register.html')

def product_detail(request, cat_slug, pro_slug):
    product = get_object_or_404(Product, category__slug=cat_slug, slug=pro_slug)
    return render(request, 'product-detail.html', {'product': product})


def place_order(request):
    return render(request,'place.html') 
def ordercomp(request):
    return render(request,'order_complete.html') 
def add_to_cart(request, ):
    return render(request, 'cart.html')
def password_reset_view(request):
    return render(request, 'password_reset.html')
