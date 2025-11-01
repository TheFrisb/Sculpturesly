from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from products.models import *


# Register your models here.
@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("title", "slug", "parent")
    search_fields = ("title", "slug")
    list_filter = ("parent",)
    fields = ("title", "slug", "parent", "description")
    readonly_fields = ("slug",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image",)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = (
        "sku",
        "height",
        "width",
        "length",
        "stock_quantity",
        "color",
        "image",
        "categories",
        "external_url",
    )
    autocomplete_fields = ("categories",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "price_start", "created_at")
    search_fields = ("title", "slug")
    list_filter = ("status",)
    autocomplete_fields = ("categories",)
    fields = ("status", "title", "slug", "image", "categories", "price_start")
    readonly_fields = ("slug",)
    inlines = (ProductVariantInline,)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "product",
        "stock_quantity",
        "color",
        "regular_price",
        "created_at",
    )
    search_fields = ("sku", "product__title")
    list_filter = ("product",)
    autocomplete_fields = ("product", "categories")
    fields = (
        "product",
        "sku",
        "height",
        "width",
        "length",
        "stock_quantity",
        "color",
        "image",
        "categories",
        "regular_price",
        "external_url",
    )
    inlines = (ProductImageInline,)
