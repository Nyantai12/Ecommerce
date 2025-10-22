from .models import Cart, CartItem

def cart_counter(request):
    count = 0
    cart_id = request.session.session_key
    if cart_id:
        try:
            cart = Cart.objects.get(cart_id=cart_id)
            count = sum(item.quantity for item in CartItem.objects.filter(cart=cart, is_active=True))
        except Cart.DoesNotExist:
            count = 0
    return {'cart_item_count': count}
