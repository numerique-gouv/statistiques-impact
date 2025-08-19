from rest_framework import permissions
from rest_framework import exceptions
from core import models
from django.shortcuts import get_object_or_404

from django.utils.translation import gettext_lazy as _


class HasValidAPIKeyOrReadOnly(permissions.BasePermission):
    """
    Give access to requests bearing the right API key for the product.
    """

    def has_permission(self, request, view):
        """Custom permission to check if method is safe OR is request is using valid API Key for this product."""
        if request.method in permissions.SAFE_METHODS:
            return True

        product = get_object_or_404(models.Product, slug=view.kwargs["product_slug"])
        if key := request.headers.get("X-Api-Key"):
            try:
                api_key = models.ProductAPIKey.objects.get_from_key(key)
            except models.ProductAPIKey.DoesNotExist:
                raise exceptions.PermissionDenied(_("Invalid API Key"))

            if api_key.product == product:
                return True

        return False
