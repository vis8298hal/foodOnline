from django.db import models
from vendor.models import Vendor

# Create your models here.
class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, unique=False)
    slug = models.SlugField(max_length=100,unique=False)
    description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        constraints = [
            models.UniqueConstraint(fields=['vendor', 'category_name', "slug"], name='unique_item_category')
        ]

    def clean(self):
        self.category_name = self.category_name.capitalize()
    def __str__(self):
        return self.category_name

class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    food_title = models.CharField(max_length=150)
    item_slug = models.SlugField(max_length=100,unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    image = models.ImageField(upload_to="foodItems")
    is_available = models.BooleanField(default=True)
    on_hand_quantity = models.IntegerField(default=1)
    description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_veg = models.BooleanField(default=False)

    def __str__(self):
        return self.food_title