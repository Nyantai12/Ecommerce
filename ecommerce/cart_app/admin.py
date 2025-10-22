from django.contrib import admin
from .models import Cart, CartItem

# Cart admin
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'created_date', 'total_items', 'total_price')
    readonly_fields = ('cart_id', 'created_date', 'total_items', 'total_price')

    # CartItem-уудыг нэгтгэн тоолох функцууд
    def total_items(self, obj):
        return sum(item.quantity for item in CartItem.objects.filter(cart=obj, is_active=True))
    total_items.short_description = 'Total Items'

    def total_price(self, obj):
        return sum(item.quantity * item.product.price for item in CartItem.objects.filter(cart=obj, is_active=True))
    total_price.short_description = 'Total Price'

# CartItem админ
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')
    list_filter = ('cart', 'is_active')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
