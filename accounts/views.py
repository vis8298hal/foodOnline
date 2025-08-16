from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from django.contrib import messages
# Create your views here.

def registerUser(request):
    if request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            #Create User using form

            #password = form.cleaned_data['password']
            #user = form.save(commit=False)
            #user.set_password(password)
            #user.role = User.CUSTOMER
            #user.save()
            #

            #Create User using model method create_user
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your account has been registered successfully")
            return redirect('registerUser')
        else:
            print("Invalid form")
            print(form.errors)
    else:
        form = UserForm()
    context = {
            "form": form
        }
    return render(request, 'accounts/registerUser.html', context=context)

def registerVendor(request):
    
    if request.method == "POST":
        form = UserForm(request.POST)
        vForm = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vForm.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.role = User.VENDOR
            user.save()
            user_profile = UserProfile.objects.get(user=user)
            vendor = vForm.save(commit=False)
            vendor.user = user
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your account has been registered successfully! Please wait for approval")
            return redirect('registerVendor')
        else:
            print("Invalid Forms")
            print(form.errors)
            print(vForm.errors)
    else:
        form = UserForm()
        vForm = VendorForm()
    context = {
        'form': form,
        'vForm': vForm
    }
    return render(request, 'accounts/registerVendor.html', context=context)
