from rest_framework.generics import ListAPIView

from sections.models import FeaturedProduct
from sections.serializers import FeaturedProductSerializer


class FeaturedProductsListView(ListAPIView):
    serializer_class = FeaturedProductSerializer

    def get_queryset(self):
        return FeaturedProduct.objects.all().order_by("sort_order")
