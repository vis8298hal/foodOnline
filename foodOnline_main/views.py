from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import Vendor
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D 
from django.contrib.gis.db.models.functions import Distance

def get_or_set_current_location(request):
    if 'lat' in request.session:
        lattitude = request.session["lat"]
        longitude = request.session["lng"]
        return longitude, lattitude
    elif 'lat' in request.GET:
        lattitude = request.GET.get("lat")
        longitude = request.GET.get("lng")
        request.session["lat"] = lattitude
        request.session["lng"] = longitude
        return longitude, lattitude
    else:
        return None

def home(request):
    if get_or_set_current_location(request) is not None:
        #print(lattitude, longitude)
        point = GEOSGeometry("POINT(%s %s)"%(get_or_set_current_location(request)), srid=4326)
        print(get_or_set_current_location(request))
        vendors  = Vendor.objects.filter( is_approved = True,  user_profile__location__distance_lte=(point, D(km=50))).annotate(distance=Distance("user_profile__location", point)).order_by("distance")
        for v in vendors:
            print(v.is_open)
            v.kms = round(v.distance.km, 2)
        print("By location Enabled Vendor")
    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
        print([vendor.is_open for vendor in vendors])
    context = {
        "vendors": vendors
    }
    return render(request, "home.html", context=context)