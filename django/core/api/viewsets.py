from rest_framework import viewsets, mixins, exceptions
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from core import models
from core.api import serializers, permissions
from django.core.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser
from django.shortcuts import get_object_or_404
from core.clients.datagouv import DataGouvClient


class ProductViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    API endpoint to list existing products.

    - GET products/ lists all product
    - GET products/<product_slug>/ retrieves info on this product
    """

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    lookup_field = "slug"

    def get_serializer_class(self):
        """Return list or detail serializer depending on the action."""
        if self.action == "retrieve":
            return serializers.ProductDetailSerializer

        return self.serializer_class


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

    serializer_class = serializers.IndicatorDetailSerializer

    # serializer_list_class = serializers.IndicatorListSerializer
    # serializer_detail_class = serializers.IndicatorDetailSerializer
    queryset = models.Indicator.objects.all()
    permission_classes = [permissions.HasValidAPIKeyOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()

        if product_slug := self.kwargs.get("product_slug"):
            product = get_object_or_404(models.Product, slug=product_slug)
            queryset = queryset.filter(productid=product)

        return queryset

    def get_serializer_context(self):
        """Extra context provided to the serializer class."""
        context = super().get_serializer_context()
        context["product_slug"] = self.kwargs["product_slug"]
        return context

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
        file = request.FILES["file"]

        product = get_object_or_404(models.Product, slug=kwargs["product_slug"])

        if product.slug not in ["france-transfert", "france-transfert-tests"]:
            raise exceptions.MethodNotAllowed(
                method="Submission",
                detail="File submission not authorized for this product.",
            )

        env = "demo" if product.slug == "france-transfert-tests" else "www"

        client = DataGouvClient(adaptor=models.Adaptor(product=product), env=env)
        response = client.upload_new_file(file=file.file.getvalue(), filename=file.name)
        return Response(
            data={"file": file.name, "success": response.json()["success"]},
            status=response.status_code,
        )


class RecordViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint to list and manage indicators' record of a given product.

    POST /api/products/<product-slug>/indicators/<indicator-slug>/records/
        Return newly added record

    GET /api/products/<product-slug>/indicators/<indicator-slug>/records/
        Return a list of records for this indicator

    GET /api/products/<product-slug>/indicators/<indicator-slug>/records/<record_id>/
        Return details on a single record

    DELETE /api/products/<product-slug>/indicators/<indicator-slug>/records/<record_id>/
    """

    serializer_class = serializers.RecordSerializer
    queryset = models.Record.objects.all()
    permission_classes = [permissions.HasValidAPIKeyOrReadOnly]
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        """Filter queryset by product and possibly indicator."""
        indicator = get_object_or_404(
            models.Indicator,
            slug=self.kwargs.get("indicator_slug"),
            productid__slug=self.kwargs.get("product_slug"),
        )
        queryset = super().get_queryset().filter(indicator=indicator)
        return queryset

    def get_serializer_context(self):
        """Extra context provided to the serializer class."""
        context = super().get_serializer_context()
        context["product_slug"] = self.kwargs["product_slug"]
        context["indicator_slug"] = self.kwargs["indicator_slug"]
        return context
