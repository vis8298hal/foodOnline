from django import forms
from .models import Category, FoodItem
from accounts.validators import allow_only_images_validator

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "description"]

class FoodItemForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_only_images_validator], required=False)
    is_available = forms.BooleanField(required=False)
    is_veg = forms.BooleanField(required=False)
    
    class Meta:
        model = FoodItem
        fields = ["food_title", "description", "image", "price", "on_hand_quantity", "is_veg", "category", "is_available"]

    