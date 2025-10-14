from django.contrib import admin
from core import models
from rest_framework_api_key.admin import APIKeyModelAdmin


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin interface declaration."""

    list_display = ("nom_service_public_numerique", "last_indicators_date")
    readonly_fields = ("id",)
    prepopulated_fields = {"slug": ("nom_service_public_numerique",)}


@admin.register(models.Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    """Indicator admin interface declaration."""

    list_display = (
        "productid__nom_service_public_numerique",
        "indicateur",
        "date",
        "frequence_monitoring",
        "valeur",
    )
    search_fields = ("productid__nom_service_public_numerique", "indicateur")
    list_filter = [
        "productid__nom_service_public_numerique",
        "indicateur",
        ("date", admin.DateFieldListFilter),
    ]
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(models.ProductAPIKey)
class ProductAPIKeyAdmin(APIKeyModelAdmin):
    """Api keys admin interface declaration."""

    list_display = [
        *APIKeyModelAdmin.list_display,
        "product__nom_service_public_numerique",
    ]
    search_fields = [
        *APIKeyModelAdmin.search_fields,
        "product",
    ]
    fields = [
        "prefix",
        "name",
        "expiry_date",
        "revoked",
        "product",
    ]
    readonly_fields = ["prefix", "created"]
