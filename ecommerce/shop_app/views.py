from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Category, Product  # <- Үүнийг заавал нэмнэ

def index(request):
    categories = Category.objects.all()  # Admin-д байгаа бүх category
    popular_products = Product.objects.all()[:8]  # Жишээ: хамгийн эхний 8 product
    context = {
        'categories': categories,
        'popular_products': popular_products
    }
    return render(request, 'index.html', context)
def cart_view(request):
    return render(request, 'cart.html')

def store(request):
    return render(request, 'store.html', )
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