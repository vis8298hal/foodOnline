from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from .models import Vendor
from accounts.views import check_role_vendor
from accounts.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from foodmenu.models import Category, FoodItem
from foodmenu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify

# Helper Function
def get_vendor(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    return vendor
# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES,instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "The Restaurant has been updated")
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        "profile_form": profile_form,
        "vendor_form": vendor_form,
        "profile": profile,
        "vendor": vendor,
    }
    return render(request, "vendor/vprofile.html", context=context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor).order_by("created_at")
    context = {"categories": categories}
    return render(request, "vendor/menu_builder.html", context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def food_item_by_category(request, pk=None):
    vendor = Vendor.objects.get(user=request.user)
    category = get_object_or_404(Category,pk=pk)
    fooditems = FoodItem.objects.filter(category=category)
    context = {
        "foodItems": fooditems,
        "category": category,
    }
    return render(request, "vendor/fooditem_by_category.html", context=context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        try:
            if form.is_valid():
                
                    category_name = form.cleaned_data["category_name"]
                    category = form.save(commit=False)
                
                    category.vendor = get_vendor(request)
                    category.slug = slugify(category_name)
                    form.save()
                    messages.success(request, "Category Added Successfully")
                    return redirect("menu-builder")
            else:
                print(form.errors)
        except Exception as e:
            messages.error(request, e)
    else:
        form = CategoryForm()
    context = {
        "category_form":form
    }
    return render(request, "vendor/add_category.html", context=context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        try:
            if form.is_valid():
                
                    category_name = form.cleaned_data["category_name"]
                    category = form.save(commit=False)
                
                    category.vendor = get_vendor(request)
                    category.slug = slugify(category_name)
                    form.save()
                    messages.success(request, "Category Added Successfully")
                    return redirect("menu-builder")
            else:
                print(form.errors)
        except:
            messages.error(request, "Category Already  Exists")
    else:
        form = CategoryForm(instance=category)
    context = {
        "category_form":form,
        "category": category
    }
    return render(request, "vendor/edit_category.html", context=context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    if pk is not None:
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, f"Category {category.category_name} is deleted Successfully")
        
    else:
        messages.error("Invalid Category : This Category can't be deleted please contact support team")
    return redirect("menu-builder")

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_fooditem(request):
    vendor = get_vendor(request)
    if request.method == "POST":
        fooditem_form = FoodItemForm(request.POST, request.FILES)
        if fooditem_form.is_valid():
            food_title = fooditem_form.cleaned_data["food_title"]
            food = fooditem_form.save(commit=False)
            food.vendor = vendor
            food.slug = slugify(food_title)
            if food.on_hand_quantity > 0:
                food.is_available =True
            else:
                food.is_available = False
            
            fooditem_form.save()
            messages.success(request, "Food Item Saved successfully")
            return redirect('food_item_by_category', food.category.pk)
    else:
        fooditem_form = FoodItemForm()
        fooditem_form.fields["category"].queryset = Category.objects.filter(vendor=get_vendor(request))
        messages.success(request, "Categories")
    context = {
        "fooditem": fooditem_form,

    }
    return render(request, "vendor/add_fooditem.html", context=context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_fooditem(request, pk):
    food = get_object_or_404(FoodItem,pk=pk)
    print(food)
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            food_title = form.cleaned_data["food_title"]
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            if food.on_hand_quantity > 0:
                food.is_available =True
            else:
                food.is_available = False
            form.save()
            messages.success(request, f"The Food Item : {food_title} has been modified successfully")
            return redirect('food_item_by_category', food.category.pk)
    else:
        form = FoodItemForm(instance=food)
        form.fields["category"].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        "fooditem": form,
        "food": food,

    }

    return render(request, "vendor/edit_fooditem.html", context=context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_fooditem(request, pk):
    if pk is not None:
        fooditem = get_object_or_404(FoodItem, pk=pk)
        fooditem.delete()
        messages.success(request, f"FoodItem: {fooditem.food_title} is deleted Successfully")
        return redirect('food_item_by_category', fooditem.category.pk)
        
    else:
        messages.error("Invalid FoodItem : This FoodItem can't be deleted please contact support team")
        return redirect("menu-builder")