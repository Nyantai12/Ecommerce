from django.db import models
from django.contrib.auth.models import User
from shop_app.models import Product

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.product)
