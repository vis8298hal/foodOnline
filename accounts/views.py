from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detect_user, send_accounts_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils .http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
# Restrict Permissions of Vendor
def check_role_vendor(user):
    if user.role == 1:
        print( "Go to Vendor Dashboard as per successful login")
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
    current_site = get_current_site(request)
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
            context_em = {
        'user': user,
        'token': default_token_generator.make_token(user),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'domain': current_site,
    }
            send_accounts_email(user, template='accounts/emails/account_verification_email.html', subject="Please activate your account", context=context_em)
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
    current_site = get_current_site(request)
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
            context_em = {
        'user': user,
        'token': default_token_generator.make_token(user),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'domain': current_site,
    }
            #print(context)
            send_accounts_email(user, template='accounts/emails/account_verification_email.html', 
                                subject="Please activate your account", context=context_em)
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

def activate(request, uidb64, token):
    """Activate the user by toggling is_active status"""
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations Your Account is activated")
        return redirect('myAccount')
    else:
        messages.error(request, "Invalid Activation Link")
        return redirect("myAccount")
    
def forgot_password(request):
    current_site = get_current_site(request)
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            context_em = {
        'user': user,
        'token': default_token_generator.make_token(user),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'domain': current_site,
    }
            send_accounts_email( user=user, template="accounts/emails/reset_password_email.html",
                                 subject="Reset your Password", context=context_em)
            messages.success(request, "Password Reset Link has been sent to your registered email address")
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, "accounts/forgot_password.html")

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid.decode('utf-8')
        messages.info(request, "Please Reset Your Password")
        return redirect("reset_password")
    else:
        messages.error(request, "This Link has been expired.")
        return redirect("myAccount")
    return HttpResponse("accounts/reset_password.html")

def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            uid = request.session.get("uid")
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password Reset Successful")
            return redirect("login")
        else:
            messages.error(request, "Passwords don't Match ")
            return redirect("reset_password")
    return render(request, "accounts/reset_password.html")