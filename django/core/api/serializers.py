from core.models import Product, Indicator
from rest_framework import serializers


class IndicatorSerializer(serializers.ModelSerializer):
    valeur = serializers.IntegerField()

    class Meta:
        model = Indicator
        fields = "__all__"
        read_only_fields = [
            "productid",
        ]

    def validate(self, attrs):
        product = Product.objects.filter(
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
        model = Product
        fields = ["nom_service_public_numerique", "slug", "last_indicators"]

    def get_last_indicators(self, instance):
        return IndicatorSerializer(instance.last_indicators, many=True).data


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["nom_service_public_numerique", "slug"]
