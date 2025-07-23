from rest_framework import viewsets, mixins
from core import models
from core.api import serializers


class ProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows to list existing products.
    """

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
