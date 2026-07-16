from django.contrib import admin
from core import models
from rest_framework_api_key.admin import APIKeyModelAdmin


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin interface declaration."""

    list_display = ("name", "last_indicators_date")
    readonly_fields = ("id",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    """Indicator admin interface declaration."""

    list_display = (
        "productid__name",
        "indicateur",
        "date",
        "frequence_monitoring",
        "valeur",
    )
    search_fields = ("productid__name", "indicateur")
    list_filter = [
        "productid__name",
        "indicateur",
        ("date", admin.DateFieldListFilter),
    ]
    readonly_fields = ("id", "created_at", "updated_at", "slug")


@admin.register(models.ProductAPIKey)
class ProductAPIKeyAdmin(APIKeyModelAdmin):
    """Api keys admin interface declaration."""

    list_display = [
        *APIKeyModelAdmin.list_display,
        "product__name",
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


@admin.register(models.Adaptor)
class AdaptorAdmin(admin.ModelAdmin):
    """Administration view to manage adaptors to automatically fetch products' data."""

    list_display = (
        "product",
        "indicator",
        "status",
    )
    search_fields = ("product", "indicator")
    list_filter = [
        "product",
        "indicator",
        "status",
    ]
    readonly_fields = ["status", "created_at"]


@admin.register(models.Record)
class RecordAdmin(admin.ModelAdmin):
    """Indicator admin interface declaration."""

    list_display = (
        "indicator",
        "end_date",
        "value",
    )
    search_fields = ("indicator",)
    list_filter = [
        "indicator",
        ("end_date", admin.DateFieldListFilter),
    ]
    readonly_fields = ("id", "created_at", "updated_at")
