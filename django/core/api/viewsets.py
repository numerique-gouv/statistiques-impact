from rest_framework import viewsets, mixins, permissions
from core import models
from core.api import serializers
from rest_framework_api_key.permissions import HasAPIKey


class ProductViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    API endpoint to list existing products.
    """

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = "slug"


class IndicatorViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint to list and manage indicators of a given product.
    """

    serializer_class = serializers.IndicatorSerializer
    queryset = models.Indicator.objects.all()
    permission_classes = [HasAPIKey | permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if product_slug := self.kwargs.get("product_id"):
            product = models.Product.objects.get(slug=product_slug)
            queryset = queryset.filter(productid=product)
        return queryset
