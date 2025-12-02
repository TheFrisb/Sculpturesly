from django.urls import path

from .views import FeaturedCategoryListView, FeaturedProductsListView

urlpatterns = [
    path(
        "featured-products/",
        FeaturedProductsListView.as_view(),
        name="featured-products-list",
    ),
    path(
        "featured-categories/",
        FeaturedCategoryListView.as_view(),
        name="featured-category-list",
    ),
]
