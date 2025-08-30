from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import JsonResponse
from vendor.models import Vendor
from foodmenu.models import Category, FoodItem
from django.db.models import Prefetch
from .models import Cart
from .context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    vendor_count = vendors.count()
    context = {
        "vendors": vendors,
        "vendor_count": vendor_count,
    }
    return render(request, "marketplace/listings.html", context=context)

def vendor_detail(request, vendor_slug):
    vendor_detail = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor_detail).prefetch_related(
        Prefetch("foodItem",
                 queryset = FoodItem.objects.filter(is_available=True))
    )
    print(vendor_detail)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        "vendor": vendor_detail,
        "categories": categories,
        "cart_items": cart_items,
    }
    return render(request, "marketplace/vendor_detail.html", context=context)

def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                food = FoodItem.objects.get(pk=food_id)
                print(food.food_title)
                try:
                    # if Item is already available in cart
                    chkCart = Cart.objects.get(user=request.user, food_item=food)
                    if chkCart.quantity > 0:
                        chkCart.quantity += 1
                        chkCart.save()
                        return JsonResponse({
                        "status": "Success",
                        "message": "Cart quantity Increased",
                        "cart_counter": get_cart_counter(request),
                        "qty": chkCart.quantity,
                        "cart_amounts": get_cart_amounts(request),
                    })
                    else:
                        chkCart = Cart.objects.create(user=request.user, food_item=food, quantity=1)
                        chkCart.save()
                        return JsonResponse({
                        "status": "Success",
                        "message": "Item  Added to Cart",
                        "cart_counter": get_cart_counter(request),
                        "qty": chkCart.quantity,
                        "cart_amounts": get_cart_amounts(request),
                    })
                except:
                    chkCart = Cart.objects.create(user=request.user, food_item=food, quantity=1)
                    chkCart.save()
                    return JsonResponse({
                    "status": "Success",
                    "message": "Item  Added to Cart",
                    "cart_counter": get_cart_counter(request),
                    "qty": chkCart.quantity,
                    "cart_amounts": get_cart_amounts(request),
                })
                
            except:
                return JsonResponse({
                    "status": "Failed",
                    "message": "Item  Not Available",
                })
        else:
            return JsonResponse({
            "status": "Failed",
            "message": "Invalid Request",
        })
            
    else:
        return JsonResponse({
            "status": "login_required",
            "message": "Please Login to Continue",
        })

def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                food = FoodItem.objects.get(pk=food_id)
                print(food.food_title)
                try:
                    # if Item is already available in cart
                    chkCart = Cart.objects.get(user=request.user, food_item=food)
                    if  chkCart.quantity > 1:

                        chkCart.quantity -= 1
                        chkCart.save()
                        return JsonResponse({
                        "status": "Success",
                        "message": "Cart quantity Decreased",
                        "cart_counter": get_cart_counter(request),
                        "qty": chkCart.quantity,
                        "cart_amounts": get_cart_amounts(request),
                    })
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                        return JsonResponse({
                        "status": "Success",
                        "message": "Removed from Cart",
                        "cart_counter": get_cart_counter(request),
                        "qty": 0,
                        "cart_amounts": get_cart_amounts(request),
                    })
                except:
                    
                    return JsonResponse({
                    "status": "Failed",
                    "message": "This item is not in the cart",
                    "qty": 0,
                })
                
            except:
                return JsonResponse({
                    "status": "Failed",
                    "message": "Item  Not Available",
                })
        else:
            return JsonResponse({
            "status": "Failed",
            "message": "Invalid Request",
        })
            
    else:
        return JsonResponse({
            "status": "login_required",
            "message": "Please Login to Continue",
        })
@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by("created_at")
    context = {
        "cart_items": cart_items,
    }
    return render(request, "marketplace/cart.html", context=context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user, pk=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({
                        "status": "Success",
                        "message": "Cart Item Deleted",
                        "cart_counter": get_cart_counter(request),
                        "qty": 0,
                        "cart_amounts": get_cart_amounts(request),
                    })
            except:
                return JsonResponse({
                    "status": "Failed",
                    "message": "Item  Not Exists",
                })
        else:
            return JsonResponse({
            "status": "Failed",
            "message": "Invalid Request",
        })
    else:
        return JsonResponse({
            "status": "login_required",
            "message": "Please Login to Continue",
        })