from .models import Cart
from foodmenu.models import FoodItem

def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0

        except:
            cart_count = 0
    return dict(cart_count=cart_count)

def get_cart_amounts(request):
    tax = 0
    subtotal = 0
    grand_total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for cart_item in cart_items:
            food_item = FoodItem.objects.get(pk=cart_item.food_item.pk)
            if food_item:
                subtotal += (food_item.price*cart_item.quantity)
        grand_total = subtotal+tax
        print(grand_total)
        return dict(subtotal=subtotal,
                    taxes=tax,
                    grand_total=grand_total)
    else:
        return dict(subtotal=0,taxes=0,grand_total=0)