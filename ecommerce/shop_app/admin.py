from django.contrib import admin
from .models import Category, ImageGallery, Product

# Category admin
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}  # ← яг Category-д байгаа field

class ProductImageInline(admin.TabularInline):
    model = ImageGallery
    extra = 1

# Product admin
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductImageInline]

# Register models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
