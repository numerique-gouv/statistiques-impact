"""API URL Configuration"""

from django.urls import include, path
from django.contrib import admin

from core import views
from . import api_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accessibility", views.accessibility, name="accessibility"),
    path(
        "api/",
        include(api_urls),
    ),
]
