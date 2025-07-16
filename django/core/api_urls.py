"""API URL Configuration"""

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from core.api import viewsets

product_router = DefaultRouter()
product_router.register("products", viewsets.ProductViewSet, basename="products")


urlpatterns = [path("", include([*product_router.urls]))]
