from django.contrib import admin
from .models import Category, Product

# Category admin
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}  # ← яг Category-д байгаа field

# Product admin
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}

# Register models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)