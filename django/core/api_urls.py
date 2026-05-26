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

record_router = SimpleRouter()
record_router.register(
    "records",
    viewsets.RecordViewSet,
    basename="records",
)

urlpatterns = [
    path("", include(product_router.urls)),
    re_path(r"^products/(?P<product_slug>[\w-]+)/?", include(record_router.urls)),
    re_path(
        r"^products/(?P<product_slug>[\w-]+)/submission/?",
        viewsets.RecordSubmissionView.as_view(),
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
