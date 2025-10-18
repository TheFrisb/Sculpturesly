from django.urls import path

from carts.views import CheckoutView

app_name = "carts"
urlpatterns = [path("checkout/", CheckoutView.as_view(), name="checkout")]
