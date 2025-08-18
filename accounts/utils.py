from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils .http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings


def detect_user(user):
    if user.role == 1:
        redirect_url = "vendorDashboard"
    elif user.role == 2:
        redirect_url = "custDashboard"
    elif user.role == None and user.is_superadmin:
        redirect_url = "/admin"
    return redirect_url

def send_accounts_email(request, user, template, subject):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = subject
    message = render_to_string(template, {
        'user': user,
        'token': default_token_generator.make_token(user),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'domain': current_site,
    })
    to_email = user.email
    mail = EmailMessage(subject=mail_subject, body=message,from_email=from_email, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()