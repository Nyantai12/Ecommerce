from django.urls import path
from . import views

urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('cart/remove/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('cart/reduce/<int:product_id>/', views.reduce_cart_item, name='reduce_cart_item'),
]
