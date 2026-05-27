from core import models
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class IndicatorListSerializer(serializers.ModelSerializer):
    """A smaller serializer for Indicator model."""

    productid = serializers.SlugRelatedField(slug_field="slug", read_only=True)

    class Meta:
        model = models.Indicator
        fields = ["slug", "productid"]
        read_only_fields = ["slug", "productid"]


class IndicatorDetailSerializer(serializers.ModelSerializer):
    """A detailed serializer for Indicator model."""

    valeur = serializers.IntegerField()
    productid = serializers.SlugRelatedField(slug_field="slug", read_only=True)

    class Meta:
        model = models.Indicator
        fields = "__all__"
        read_only_fields = [
            "productid",
        ]

    def validate(self, attrs):
        product = models.Product.objects.filter(
            slug=self.context["view"].kwargs["product_slug"]
        )
        if product.exists():
            attrs["productid"] = product[0]
        return super().validate(attrs)


class IndicatorSubmitSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()

    class Meta:
        fields = ["file_uploaded"]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for Product objects. Add most recent indicators."""

    last_indicators = serializers.SerializerMethodField("get_last_indicators")

    class Meta:
        model = models.Product
        fields = ["nom_service_public_numerique", "slug", "last_indicators"]

    def get_last_indicators(self, instance):
        return IndicatorDetailSerializer(instance.last_indicators, many=True).data


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ["nom_service_public_numerique", "slug"]


class RecordSerializer(serializers.ModelSerializer):
    """A serializer to display record information."""

    indicator = IndicatorListSerializer(read_only=True)

    class Meta:
        model = models.Record
        fields = [
            "id",
            "value",
            "start_date",
            "end_date",
            "is_auto_added",
            "created_at",
            "updated_at",
            "indicator",
        ]

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        try:
            attrs["indicator"] = get_object_or_404(
                models.Indicator, slug=self.context.get("indicator_slug")
            )
        except KeyError as exc:
            raise exceptions.ValidationError(
                "You must set a indicator slug in kwargs to create a new record."
            ) from exc

        return super().validate(attrs)
