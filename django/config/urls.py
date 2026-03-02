"""
URL configuration for stats projects
"""

from django.urls import include, path

from core import urls as core_urls


urlpatterns = [
    path("", include(core_urls)),
]
