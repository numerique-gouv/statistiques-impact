from core.models import Product, Indicator
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "nom_service_public_numerique"]


class IndicatorSerializer(serializers.ModelSerializer):
    valeur = serializers.IntegerField()

    class Meta:
        model = Indicator
        fields = "__all__"
        read_only_fields = [
            "productid",
        ]

    def validate(self, attrs):
        product = Product.objects.filter(slug=self.context["view"].kwargs["product_id"])
        if product.exists():
            attrs["productid"] = product[0]
        return super().validate(attrs)
