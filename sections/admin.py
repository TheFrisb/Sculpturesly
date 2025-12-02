from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from sections.models import FeaturedProduct


# Register your models here.
@admin.register(FeaturedProduct)
class FeaturedProductAdmin(SortableAdminMixin, admin.ModelAdmin):
    ordering = ["sort_order"]
    autocomplete_fields = ["product"]
