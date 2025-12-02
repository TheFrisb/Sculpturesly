from rest_framework import serializers

from products.serializers import ProductListSerializer
from sections.models import FeaturedProduct


class FeaturedProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = FeaturedProduct
        fields = ["product", "image"]
