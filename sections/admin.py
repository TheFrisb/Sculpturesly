from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from sections.models import HeroSection


# Register your models here.
@admin.register(HeroSection)
class HeroSectionAdmin(SortableAdminMixin, admin.ModelAdmin):
    ordering = ["sort_order"]
