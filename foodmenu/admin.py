from django.contrib import admin
from .models import Category, FoodItem
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category_name",)}
    list_display = ("category_name", "vendor", "modified_at")
    search_fields = ("category_name", "vendor__vendor_name")

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"item_slug": ("food_title",)}
    list_display = ("food_title", "category", "vendor", "on_hand_quantity", "price","modified_at")
    search_fields = ("food_title", "category__category_name", "price", "vendor__vendor_name")
    list_filter = ("is_available", "is_veg")


admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
