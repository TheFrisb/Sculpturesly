from django.urls import path

from .views import FeaturedProductsListView

urlpatterns = [
    path(
        "featured-products/",
        FeaturedProductsListView.as_view(),
        name="featured-products-list",
    )
]
