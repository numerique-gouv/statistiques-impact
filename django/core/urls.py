"""Core URL Configuration"""

from django.urls import include, path, re_path
from django.contrib import admin
from django.views.generic import TemplateView

from core import views
from . import api_urls

urlpatterns = [
    path("", TemplateView.as_view(template_name="core/index.html"), name="index"),
    path("admin/", admin.site.urls),
    re_path(
        r"accessibilite/?$",
        TemplateView.as_view(template_name="core/accessibility.html"),
        name="accessibility",
    ),
    re_path(
        r"mentions-legales/?$",
        TemplateView.as_view(template_name="core/legal_notice.html"),
        name="legal-notice",
    ),
    re_path(
        r"last_indicators/?$",
        views.last_indicators,
        name="last_indicators",
    ),
    path(
        "produits/<product_slug>/",
        views.product,
        name="produit",
    ),
    path(
        "api/",
        include(api_urls),
    ),
]
