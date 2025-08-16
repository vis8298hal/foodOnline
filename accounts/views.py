from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detect_user
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
# Restrict Permissions of Vendor
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
# Restrict Permissions of Customer
# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In")
        return redirect('myAccount')
    elif request.method == "POST":
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
            return redirect('login')
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
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In")
        return redirect('myAccount')
    elif request.method == "POST":
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
            return redirect('login')
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

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In")
        return redirect('myAccount')
    elif request.method=="POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now Logged In")
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid Login Credentials")
            return redirect('login')
    return render(request, 'accounts/login.html')
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, "You have been logged Out.")
    return redirect('login')
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, "accounts/custDashboard.html")
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, "accounts/vendorDashboard.html")
@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirect_url = detect_user(user)
    return redirect(redirect_url)