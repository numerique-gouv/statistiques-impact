from django.contrib import admin, messages
from core import models
from rest_framework_api_key.admin import APIKeyModelAdmin
from django.utils.translation import gettext_lazy as _


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
    actions = ["fetch_newest_data"]

    @admin.action()
    def fetch_newest_data(self, request, queryset):
        """Call onto adaptor's client to fetch newest data."""

        for adaptor in queryset:
            try:
                results = adaptor.save_last_month_indicator()
            except Exception as exc:
                messages.error(
                    request,
                    _("Failed to fetch new data for %(adaptor)s: %(exc)s")
                    % {"adaptor": adaptor, "exc": exc},
                )
            else:
                messages.success(
                    request,
                    _(
                        "Successfully fetched %(results)s new indicator(s) from %(adaptor)s."
                    )
                    % {"adaptor": adaptor, "number": len(results)},
                )
