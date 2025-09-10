from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.http import JsonResponse
from vendor.models import Vendor
from foodmenu.models import Category, FoodItem
from django.db.models import Prefetch
from .models import Cart
from .context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D 
from django.contrib.gis.db.models.functions import Distance
from vendor.models import OpeningHour
from datetime import datetime

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
    def_time_format = "%H:%M:%S"
    today = datetime.now()
    current_time = today.strftime(def_time_format)

    today = today.strftime("%u")
    print(today)
    vendor_detail = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    opening_hours = OpeningHour.objects.filter(vendor=vendor_detail).order_by("day", "from_hour")
    today_opening_hour = OpeningHour.objects.filter(vendor=vendor_detail, day=today)
    is_open = None
    
    for hour in today_opening_hour:
        start_time = str(datetime.strptime(hour.from_hour, "%I:%M %p").time())
        end_time = str(datetime.strptime(hour.to_hour, "%I:%M %p").time())

        if current_time > start_time and current_time < end_time:
            is_open = True
            break
        else:
            is_open = False
    print(is_open)
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
        "opening_hours": opening_hours,
        "today_opening_hour": today_opening_hour,
        "is_open": is_open,
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
    
def search(request):
    if "address" not in request.GET:
        return redirect("marketplace")
    else:
        rest_name = request.GET["keyword"]
        address = request.GET["address"]
        lattitude = request.GET["lattitude"]
        longitude = request.GET["longitude"]
        radius = request.GET["radius"]
        # Get Vendor Id which have the food Items User looking for
        vendor_by_food = FoodItem.objects.filter(food_title__icontains=rest_name, is_available=True).values_list("vendor", flat=True)

        vendors = Vendor.objects.filter(Q(id__in=vendor_by_food) | Q(vendor_name__icontains=rest_name, is_approved=True, user__is_active=True))
        if lattitude and longitude and radius:
            point = GEOSGeometry(f"POINT({longitude} {lattitude})", srid=4326)
            vendors = Vendor.objects.filter(Q(id__in=vendor_by_food) | Q(vendor_name__icontains=rest_name, is_approved=True, user__is_active=True), user_profile__location__distance_lte=(point, D(km=radius))).annotate(distance=Distance("user_profile__location", point)).order_by("distance")
        vendor_count = vendors.count()
        for vendor in vendors:
            vendor.kms = round(vendor.distance.km, 2)
        context = {
            "vendors": vendors,
            "vendor_count": vendor_count,
            "source_location": address,
        }
        return render(request, "marketplace/listings.html", context=context)