"""API URL Configuration"""

from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from core.api import viewsets

product_router = DefaultRouter()
product_router.register("products", viewsets.ProductViewSet, basename="products")

indicator_router = DefaultRouter()
indicator_router.register(
    "indicators",
    viewsets.IndicatorViewSet,
    basename="indicators",
)


urlpatterns = [
    path(
        "",
        include(
            [
                *product_router.urls,
                re_path(
                    r"^products/(?P<product_id>[\w-]+)/?",
                    include(indicator_router.urls),
                ),
            ]
        ),
    )
]
