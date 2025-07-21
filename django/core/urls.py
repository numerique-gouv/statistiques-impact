"""Core URL Configuration"""

from django.urls import path
from django.contrib import admin

from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accessibility", views.accessibility, name="accessibility"),
    path("products", views.products, name="products"),
]
