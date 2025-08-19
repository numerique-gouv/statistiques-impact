from rest_framework import viewsets, mixins, exceptions
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from core import models
from core.api import serializers, permissions
from django.core.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser
from cron_tasks.adaptors import france_transfert
from django.shortcuts import get_object_or_404


class ProductViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    API endpoint to list existing products.

    - GET products/ lists all product
    - GET products/<product_slug>/ retrieves info on this product
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

    GET /api/products/<your-product>/indicators/
        Return a list of public indicators for this product.
        Can be filtered by indicateur with ?indicateur=<your desired indicateur>
    """

    serializer_class = serializers.IndicatorSerializer
    queryset = models.Indicator.objects.all()
    permission_classes = [permissions.HasValidAPIKeyOrReadOnly]
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()

        if product_slug := self.kwargs.get("product_slug"):
            product = get_object_or_404(models.Product, slug=product_slug)
            queryset = queryset.filter(productid=product)

        query = self.request.query_params
        if indicateur := query.get("indicateur"):
            queryset = queryset.filter(indicateur=indicateur)
        return queryset

    def perform_create(self, serializer):
        """Validate uniqueness constraints after adding productid."""
        try:
            return super().perform_create(serializer)
        except ValidationError as exc:
            raise exceptions.ValidationError(exc)


class IndicatorSubmissionView(CreateAPIView):
    parser_classes = (FileUploadParser,)
    serializer_class = serializers.IndicatorSubmitSerializer
    permission_classes = [permissions.HasValidAPIKeyOrReadOnly]

    def post(self, request, *args, **kwargs):
        """An endpoint for submission of external data in .csv format."""
        product = models.Product.objects.filter(slug=kwargs["product_slug"])
        if product.exists():
            file = request.data["file"]
            adaptor = france_transfert.FranceTransfertAdaptor()
            response = adaptor.create_indicators_from_csv(file)
        return Response(data=response, status=200)
