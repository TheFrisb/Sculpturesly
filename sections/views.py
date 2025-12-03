from rest_framework.generics import ListAPIView

from sections.models import FeaturedCategory, FeaturedProduct
from sections.serializers import FeaturedCategorySerializer, FeaturedProductSerializer


class FeaturedProductsListView(ListAPIView):
    serializer_class = FeaturedProductSerializer
    pagination_class = None

    def get_queryset(self):
        return FeaturedProduct.objects.all().order_by("sort_order")


class FeaturedCategoryListView(ListAPIView):
    serializer_class = FeaturedCategorySerializer
    pagination_class = None

    def get_queryset(self):
        return FeaturedCategory.objects.all().order_by("sort_order")[:3]
