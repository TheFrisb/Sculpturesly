from rest_framework import serializers

from products.serializers import CategorySerializer, ProductListSerializer
from sections.models import FeaturedCategory, FeaturedProduct


class FeaturedProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = FeaturedProduct
        fields = ["product", "image"]


class FeaturedCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = FeaturedCategory
        fields = ["category", "image"]
