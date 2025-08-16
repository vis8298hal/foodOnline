

def detect_user(user):
    if user.role == 1:
        redirect_url = "vendorDashboard"
    elif user.role == 2:
        redirect_url = "custDashboard"
    elif user.role == None and user.is_superadmin:
        redirect_url = "/admin"
    return redirect_url