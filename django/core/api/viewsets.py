from rest_framework import viewsets, mixins, exceptions
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from core import models
from core.api import serializers, permissions
from django.core.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser
from cron_tasks.adaptors import france_transfert


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
        """Validate uniqueness constraints after adding productid."""
        try:
            return super().perform_create(serializer)
        except ValidationError as exc:
            raise exceptions.ValidationError(exc)


class IndicatorSubmissionView(UpdateAPIView):
    parser_classes = (FileUploadParser,)
    serializer_class = serializers.IndicatorSubmitSerializer

    def post(self, request, *args, **kwargs):
        """A endpoint for submission of external data."""
        product = models.Product.objects.filter(slug=kwargs["product_id"])
        if product.exists():
            file = request.data["file"]
            adaptor = france_transfert.FranceTransfertAdaptor()
            response = adaptor.create_indicators_from_csv(file)
        return Response(data=response, status=200)
