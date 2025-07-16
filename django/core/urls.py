"""Core URL Configuration"""

from django.urls import include, path, re_path
from django.contrib import admin

from core import views
from . import api_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"accessibility/?$", views.accessibility, name="accessibility"),
    re_path(r"products/?$", views.products, name="products"),
    path(
        "api/",
        include(api_urls),
    ),
]
