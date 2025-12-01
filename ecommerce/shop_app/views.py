from dbm import sqlite3
import os
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from cart_app.models import CartItem
from cart_app.views import _cart_id
from shop_app.forms import ReviewForm
from django.db.models import Avg

from .models import Category, Order, OrderProduct, Product, ReviewRating  # <- Үүнийг заавал нэмнэ
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



def has_purchased(user, product):
    return OrderProduct.objects.filter(user=user, product=product).exists()




def product_detail(request, cat_slug, pro_slug):
    product = get_object_or_404(Product, category__slug=cat_slug, slug=pro_slug)
    reviews = ReviewRating.objects.filter(product=product, status=True)
    average_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    can_review = False
    if request.user.is_authenticated:
        can_review = OrderProduct.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),  # 4.3 гэх мэт
        'can_review': can_review
    }
    return render(request, 'product-detail.html', context)



def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=product_id)
    
    if not has_purchased(request.user, product):
        messages.error(request, "Та зөвхөн худалдан авсан бараандаа review өгнө.")
        return redirect(url)
    try:
        review = ReviewRating.objects.get(user=request.user, product=product)
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review амжилттай шинэчлэгдлээ.")
    except ReviewRating.DoesNotExist:
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.product = product
            data.save()
            messages.success(request, "Таны review амжилттай хадгалагдлаа.")

    return redirect(url)




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

# def product_detail(request, cat_slug, pro_slug):
#     product = get_object_or_404(Product, category__slug=cat_slug, slug=pro_slug)
#     in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
#     return render(request, 'product-detail.html', {'product': product, 'in_cart': in_cart})


def place_order(request):
    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))
    
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity  # subtotal нэмж байна
    
    total = sum(item.subtotal for item in cart_items)
    tax = total * 0.1
    grand_total = total + tax
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'place.html', context)




def ordercomp(request):
    if request.method != 'POST':
        return redirect('cart')

    user = request.user
    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))

    if not cart_items.exists():
        return redirect('store')

    order = Order.objects.create(user=user, is_ordered=True)
    order_products = []

    total = 0
    for item in cart_items:
        op = OrderProduct.objects.create(
            order=order,
            user=user,
            product=item.product,
            quantity=item.quantity,
            ordered=True
        )
        total += item.quantity * item.product.price
        order_products.append(op)

    tax = total * 0.1
    grand_total = total + tax

    cart_items.delete()

    context = {
        'order': order,
        'order_products': order_products,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'order_complete.html', context)

def add_to_cart(request, ):
    return render(request, 'cart.html')
def password_reset_view(request):
    return render(request, 'password_reset.html')
