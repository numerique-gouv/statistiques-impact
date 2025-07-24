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
