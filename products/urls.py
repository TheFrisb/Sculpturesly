from django.urls import path

from products.views import HomeView, CategoryView, ProductDetailView

app_name = "products"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("category/<slug:slug>/", CategoryView.as_view(), name="category"),
    path("/product/<slug:slug>/", ProductDetailView.as_view(), name="product"),
]
