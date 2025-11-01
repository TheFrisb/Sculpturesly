from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from common.mixins import TitleMixin
from products.models import Product, Category
from sections.models import HeroSection


# Create your views here.
class HomeView(TitleMixin, TemplateView):
    template_name = "products/home.html"
    title = "Home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hero_sections"] = self._get_hero_sections()
        context["best_sellers"] = self._get_best_sellers()
        context["categories"] = self._get_categories_with_product_counts()

        return context

    def _get_hero_sections(self):
        return HeroSection.objects.all().order_by("sort_order")

    def _get_best_sellers(self):
        best_sellers = {
            "All": Product.objects.prefetch_related("productvariant_set").all()[:8],
        }

        return best_sellers

    def _get_categories_with_product_counts(self):
        top_categories = Category.objects.filter(parent__isnull=True)
        result = []

        for cat in top_categories:
            descendant_ids = cat.get_descendants(include_self=True).values_list(
                "id", flat=True
            )
            product_count = (
                Product.objects.filter(categories__id__in=descendant_ids)
                .distinct()
                .count()
            )
            result.append({"category": cat, "total_products": product_count})

        return result


class CategoryView(TitleMixin, TemplateView):
    template_name = "products/category_page.html"


class ProductDetailView(TitleMixin, DetailView):
    template_name = "products/product_page.html"
