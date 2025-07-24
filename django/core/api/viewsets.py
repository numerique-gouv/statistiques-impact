from rest_framework import viewsets, mixins
from core import models
from core.api import serializers


class ProductViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    API endpoint to list existing products.
    """

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = "id"


class IndicatorViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint to list and manage indicators of a given product.
    """

    serializer_class = serializers.IndicatorSerializer
    queryset = models.Indicator.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if product_id := self.kwargs.get("product_id"):
            product = models.Product.objects.get(id=product_id)
            queryset = queryset.filter(productid=product)
        return queryset
