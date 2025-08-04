from django.contrib import admin
from core import models


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
        "valeur",
    )
    readonly_fields = ("id",)
