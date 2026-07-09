"""API URL Configuration"""

from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter, SimpleRouter

from core.api import viewsets

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from drf_spectacular.views import (
    SpectacularJSONAPIView,
)

product_router = DefaultRouter()
product_router.register(r"products", viewsets.ProductViewSet, basename="products")

indicator_router = SimpleRouter()
indicator_router.register(
    "indicators",
    viewsets.IndicatorViewSet,
    basename="indicators",
)

record_router = SimpleRouter()
record_router.register(
    "records",
    viewsets.RecordViewSet,
    basename="records",
)


urlpatterns = [
    path("", include(product_router.urls)),
    re_path(r"^products/(?P<product_slug>[\w-]+)/?", include(indicator_router.urls)),
    re_path(
        r"^products/(?P<product_slug>[\w-]+)/indicators/(?P<indicator_slug>[\w-]+)/?",
        include(record_router.urls),
    ),
    re_path(
        r"^products/(?P<product_slug>[\w-]+)/submission/?",
        viewsets.IndicatorSubmissionView.as_view(),
        name="submission",
    ),
    # Schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger.json",
        SpectacularJSONAPIView.as_view(
            urlconf="core.api_urls",
        ),
        name="api-schema",
    ),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]
