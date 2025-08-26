from django.shortcuts import render, get_object_or_404
from vendor.models import Vendor
from foodmenu.models import Category, FoodItem
from django.db.models import Prefetch

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
    context = {
        "vendor": vendor_detail,
        "categories": categories,
    }
    return render(request, "marketplace/vendor_detail.html", context=context)
