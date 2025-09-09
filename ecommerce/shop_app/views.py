from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Product  # <- Үүнийг заавал нэмнэ

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def cart_view(request):
    return render(request, 'cart.html')

def store(request):
    return render(request, 'store.html', )
def signin(request):
    return render(request, 'signin.html')

def register(request):
    return render(request, 'register.html')

def product_detail(request, ):
    return render(request, 'product-detail.html',)

def place_order(request):
    return render(request,'place.html') 
def ordercomp(request):
    return render(request,'order_complete.html') 
def add_to_cart(request, ):
    return render(request, 'cart.html')
def password_reset_view(request):
    return render(request, 'password_reset.html')