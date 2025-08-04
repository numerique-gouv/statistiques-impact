from rest_framework import viewsets, mixins
from core import models
from core.api import serializers, permissions
from django.db.utils import IntegrityError
from django.core import exceptions


class ProductViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    API endpoint to list existing products.
    """

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = "slug"


class IndicatorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint to list and manage indicators of a given product.
    """

    serializer_class = serializers.IndicatorSerializer
    queryset = models.Indicator.objects.all()
    permission_classes = [permissions.HasValidAPIKeyOrReadOnly]
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if product_slug := self.kwargs.get("product_id"):
            product = models.Product.objects.get(slug=product_slug)
            queryset = queryset.filter(productid=product)
        return queryset

    def perform_create(self, serializer):
        """Set the product ."""
        product = models.Product.objects.filter(slug=self.kwargs["product_id"])
        if product.exists():
            serializer.validated_data["productid"] = product[0]

            try:
                indicator = super().perform_create(serializer)
            except IntegrityError:
                raise exceptions.ValidationError(
                    message={"NON_FIELD_ERRORS": "Cannot create duplicate key"}
                )
            return indicator
