from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart_view, name='cart'),
    path('store/', views.store, name='store'),
    path('signin/', views.signin, name='login'), 
    path('signin/', views.register, name='signin'), 
    path('register/', views.register, name='register'),
    path('product/<int:id>/', views.product_detail, name='product_detail'), 
    path('place-order/', views.place_order, name='place_order'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('ordercomp/', views.ordercomp, name='ordercomp'),
    path('category/<int:id>/', views.category_products, name='category_products'),
    
 
    
    

]
