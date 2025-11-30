from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryListView,
    CollectionListView,
    ProductViewSet,
)

router = DefaultRouter()
router.register(r"", ProductViewSet, basename="product")
urlpatterns = [
    # Categories
    path("categories/", CategoryListView.as_view(), name="category-list"),
    # Collections
    path("collections/", CollectionListView.as_view(), name="collection-list"),
    # Products
    path("", include(router.urls)),
]
