"""API URL Configuration"""

from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter, SimpleRouter

from core.api import viewsets

from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

product_router = DefaultRouter()
product_router.register(r"products", viewsets.ProductViewSet, basename="products")

indicator_router = SimpleRouter()
indicator_router.register(
    "indicators",
    viewsets.IndicatorViewSet,
    basename="indicators",
)

urlpatterns = [
    path("", include(product_router.urls)),
    re_path(r"^products/(?P<product_slug>[\w-]+)/?", include(indicator_router.urls)),
    re_path(
        r"^products/(?P<product_slug>[\w-]+)/submission/?",
        viewsets.IndicatorSubmissionView.as_view(),
        name="submission",
    ),
    # Schema
    path(
        "swagger.json",
        SpectacularJSONAPIView.as_view(
            urlconf="core.api_urls",
        ),
        name="api-schema",
    ),
    re_path(
        r"swagger/?",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="swagger-ui",
    ),
    re_path(
        r"redoc/?",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="redoc-schema",
    ),
]
