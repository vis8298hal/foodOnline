from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.myAccount, name="vendor"),
    path('profile', views.vprofile, name="vprofile"),
]
