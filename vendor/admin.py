from django.contrib import admin
from .models import Vendor
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ["vendor_name", "is_approved", "created_at", "user"]
    list_display_links = ("user", "vendor_name")
admin.site.register(Vendor,VendorAdmin)