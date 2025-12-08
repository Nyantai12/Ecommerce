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

from .models import Category, ImageGallery, Product, ReviewRating, ReviewReaction  # <- Үүнийг заавал нэмнэ
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






from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Avg



def product_detail(request, cat_slug, pro_slug):
    product = get_object_or_404(Product, category__slug=cat_slug, slug=pro_slug)
    reviews = ReviewRating.objects.filter(product=product, )
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    can_review = False
    if request.user.is_authenticated:
        exists = ReviewRating.objects.filter(user=request.user, product=product).exists()
        if not exists:
            can_review = True

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'product_images': ImageGallery.objects.filter(product=product),
        'can_review': can_review,
    }
    return render(request, 'product-detail.html', context)




def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    url = request.META.get('HTTP_REFERER')
    review_qs = ReviewRating.objects.filter(user=request.user, product=product)
    if review_qs.exists():
        review = review_qs.first()
    else:
        review = ReviewRating(user=request.user, product=product)
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
        form.save()
        messages.success(request, "Таны review амжилттай илгээгдлээ.")
    else:
        messages.error(request, "Алдаа: rating эсвэл review талбар дутуу байна.")

    return redirect(url)





def review_react(request, review_id, action):
    if not request.user.is_authenticated:
        return redirect('signin') 
    review = get_object_or_404(ReviewRating, id=review_id)
    reaction_value = 1 if action == "like" else -1
    existing = ReviewReaction.objects.filter(review=review, user=request.user).first()
    if existing:
        if existing.reaction == reaction_value:
            existing.delete()  
        else:
            existing.reaction = reaction_value
            existing.save()
    else:
        ReviewReaction.objects.create(review=review, user=request.user, reaction=reaction_value)
    return redirect(request.META.get('HTTP_REFERER', '/'))
    






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
    return render(request, 'place.html', )

def ordercomp(request):
    return render(request, 'order_complete.html', )

def add_to_cart(request, ):
    return render(request, 'cart.html')
def password_reset_view(request):
    return render(request, 'password_reset.html')





# products/views.py

# 1.ImageGalery → буруу бичигдсэн.

# 2.pro_slg → тайлбаргүй, тодорхойгүй, жишиг нэршил зөрчсөн.
# ✔ Зөв нэр: pro_slug

# 3. slg гэдэг field байхгүй.
# ✔ Зөв: slug=pro_slug

# 4. .object → Django-д байхгүй.
# ✔ Зөв: .objects

# 5. rate — model дээр байхгүй бол буруу
# 'rating__avg' — aggregate нэртэй таарахгүй
# "0" — 0-г string болгосон → дараа нь round() дээр алдаа унах магадлалтай.
# ✔ Зөв field: 'rating'
# ✔ Зөв default: 0

# 6. Flase → Python-д байхгүй keyword.
# ✔ Зөв: False

# 7. : bhgvi ajillahgvi

# 8. prod → байхгүй field
# exist() → байхгүй function (зөв: .exists())

# 9.  1 → integer
# Python boolean биш.
# ✔ Зөв: True


# 10. productt → буруу нэр.
# ✔ Зөв: product