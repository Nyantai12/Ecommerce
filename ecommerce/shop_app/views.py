from dbm import sqlite3
import os
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from cart_app.models import CartItem
from cart_app.views import _cart_id


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



def search(request):
    keyword = request.GET.get('keyword', '').strip()
    products = Product.objects.none()
    count = 0

    if keyword:
        products = Product.objects.filter(
            Q(product_name__icontains=keyword) |
            Q(description__icontains=keyword)
        )
        count = products.count()
    paginator = Paginator(products, 4)  
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    categories = Category.objects.all()  
    context = {
        'popular_products': products_page,  
        'categories': categories,
        'count': count,
        'keyword': keyword,
    }

    return render(request, "store.html", context)





def cart_view(request):
    return render(request, 'cart.html')


def store(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_ids = request.GET.getlist('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if category_ids:
        products = products.filter(category__id__in=category_ids)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    context = {
        'popular_products': products_page,
        'categories': categories,
        'selected_categories': category_ids,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
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
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    return render(request, 'product-detail.html', {'product': product, 'in_cart': in_cart})



def place_order(request):
    return render(request,'place.html') 
def ordercomp(request):
    return render(request,'order_complete.html') 
def add_to_cart(request, ):
    return render(request, 'cart.html')
def password_reset_view(request):
    return render(request, 'password_reset.html')
