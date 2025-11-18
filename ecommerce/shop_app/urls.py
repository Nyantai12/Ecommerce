from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('<slug:cat_slug>/<slug:pro_slug>', views.product_detail, name='product_detail'),
    path('place-order/', views.place_order, name='place_order'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('ordercomp/', views.ordercomp, name='ordercomp'),
    path('store/<slug:slug>/', views.category_products, name='category_products'),
    path('search/', views.search, name='search'),

    
]
