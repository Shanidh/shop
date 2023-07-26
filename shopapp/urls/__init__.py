from django.urls import re_path as url
from django.conf.urls import include
from django.urls import path

app_name = "shopapp"

urlpatterns = [
    url("", include("shopapp.urls.shop")),
    url("customer/", include("shopapp.urls.customer")),
]