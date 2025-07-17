"""
URL configuration for stats projects
"""

from django.urls import include, path, re_path
from django.conf import settings

from core import urls as core_urls

from revproxy.views import ProxyView

urlpatterns = [
    path("", include(core_urls)),
    re_path(r"(?P<path>.*)", ProxyView.as_view(upstream=settings.UPSTREAM_EXPRESS)),
]
