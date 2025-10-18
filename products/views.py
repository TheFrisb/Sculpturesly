from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from common.mixins import TitleMixin


# Create your views here.
class HomeView(TitleMixin, TemplateView):
    template_name = "products/home.html"
    title = "Home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class CategoryView(TitleMixin, TemplateView):
    template_name = "products/category_page.html"


class ProductDetailView(TitleMixin, DetailView):
    template_name = "products/product_page.html"
