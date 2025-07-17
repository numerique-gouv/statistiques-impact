from rest_framework import permissions, viewsets
from core import models
from core.api import serializers


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to list existing products.
    """

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
