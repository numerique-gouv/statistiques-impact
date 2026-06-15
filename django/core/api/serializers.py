from core import models
from rest_framework import serializers
from django.template.defaultfilters import slugify


class RecordSerializer(serializers.ModelSerializer):
    valeur = serializers.IntegerField()

    class Meta:
        model = models.Record
        fields = "__all__"
        read_only_fields = ["productid", "slug"]

    def validate_slug(self, value):
        """Force slug field."""
        return slugify(self.indicateur)

    def validate(self, attrs):
        product = models.Product.objects.filter(
            slug=self.context["view"].kwargs["product_slug"]
        )
        if product.exists():
            attrs["productid"] = product[0]
        return super().validate(attrs)


class RecordSubmitSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()

    class Meta:
        fields = ["file_uploaded"]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for Product objects. Add most recent records."""

    last_records = serializers.SerializerMethodField("get_last_records")

    class Meta:
        model = models.Product
        fields = ["nom_service_public_numerique", "slug", "last_records"]

    def get_last_records(self, instance):
        return RecordSerializer(instance.last_records, many=True).data


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ["nom_service_public_numerique", "slug"]
