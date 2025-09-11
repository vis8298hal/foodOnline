from .models import Cart, Tax
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
    tax_dict = dict()
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for cart_item in cart_items:
            food_item = FoodItem.objects.get(pk=cart_item.food_item.pk)
            if food_item:
                subtotal += (food_item.price*cart_item.quantity)
        get_tax = Tax.objects.filter(is_active=True)
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage*subtotal)/100,2)
            tax_dict[tax_type] = {str(tax_percentage):tax_amount}
        print(tax_dict)
        for key in tax_dict.values():
            for x in key.values():
                tax += x
        grand_total = subtotal+tax
        print(grand_total)
        return dict(subtotal=subtotal,
                    taxes=tax,
                    grand_total=grand_total,
                    tax_dict=tax_dict)
    else:
        return dict(subtotal=0,taxes=0,grand_total=0)