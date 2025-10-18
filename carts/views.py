from django.shortcuts import render
from django.views.generic import DetailView

from common.mixins import TitleMixin


# Create your views here.
class CheckoutView(TitleMixin, DetailView):
    template_name = "carts/checkout.html"
    title = "Checkout"
