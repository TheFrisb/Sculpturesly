import json

from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.html import mark_safe
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


class AdminImagePreviewMixin:
    def preview_image(self, obj):
        image_field = getattr(obj, "image", None) or getattr(obj, "thumbnail", None)

        if image_field:
            return mark_safe(
                f'<img src="{image_field.url}" style="height: 50px; width: auto; border-radius: 4px; border: 1px solid #ddd;" />'
            )
        return "-"

    preview_image.short_description = "Preview"


class PrettyJSONWidget(Textarea):
    def format_value(self, value):
        try:
            if isinstance(value, str):
                value = json.loads(value)
            return json.dumps(value, indent=4, sort_keys=True)
        except (TypeError, json.JSONDecodeError):
            return value


class ProductGalleryImageInline(AdminImagePreviewMixin, admin.TabularInline):
    model = ProductGalleryImage
    extra = 1
    fields = ["preview_image", "image", "alt_text", "is_feature", "variant"]
    readonly_fields = ["preview_image"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "variant":
            if request.resolver_match.kwargs.get("object_id"):
                product_id = request.resolver_match.kwargs.get("object_id")
                kwargs["queryset"] = ProductVariant.objects.filter(
                    product_id=product_id
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductVariantInline(AdminImagePreviewMixin, admin.StackedInline):
    model = ProductVariant
    extra = 0
    show_change_link = True
    fields = (
        ("sku", "stock_quantity", "price", "compare_at_price"),
        ("image", "preview_image"),
        "attributes",
    )
    readonly_fields = ["preview_image"]

    formfield_overrides = {
        models.JSONField: {
            "widget": PrettyJSONWidget(
                attrs={"style": "width: 100%; height: 150px; font-family: monospace;"}
            )
        },
    }


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "get_choices_preview"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

    formfield_overrides = {
        models.JSONField: {
            "widget": PrettyJSONWidget(
                attrs={"style": "width: 100%; height: 100px; font-family: monospace;"}
            )
        },
    }

    def get_choices_preview(self, obj):
        if obj.choices:
            return ", ".join([str(c) for c in obj.choices[:5]]) + (
                "..." if len(obj.choices) > 5 else ""
            )
        return "-"

    get_choices_preview.short_description = "Valid Choices"


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    filter_horizontal = ["allowed_attributes"]
    search_fields = ["name"]


@admin.register(Collection)
class CollectionAdmin(AdminImagePreviewMixin, admin.ModelAdmin):
    list_display = ["title", "slug", "is_active", "preview_image"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["products"]
    readonly_fields = ["preview_image"]


@admin.register(Product)
class ProductAdmin(AdminImagePreviewMixin, admin.ModelAdmin):
    list_display = [
        "title",
        "product_type",
        "status",
        "base_price",
        "preview_image",
        "variant_count",
    ]
    list_filter = ["status", "product_type", "created_at"]
    search_fields = ["title", "slug", "specifications"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["categories"]

    fieldsets = (
        (
            "General Info",
            {
                "fields": (
                    ("title", "slug"),
                    "product_type",
                    "status",
                    "description",
                )
            },
        ),
        (
            "Media & Categorization",
            {
                "fields": (
                    ("thumbnail", "preview_image"),
                    "categories",
                )
            },
        ),
        (
            "Pricing & Specs",
            {
                "fields": (
                    "base_price",
                    "specifications",
                )
            },
        ),
    )

    readonly_fields = ["preview_image"]
    inlines = [ProductGalleryImageInline, ProductVariantInline]

    formfield_overrides = {
        models.JSONField: {
            "widget": PrettyJSONWidget(
                attrs={"style": "width: 100%; height: 200px; font-family: monospace;"}
            )
        },
    }

    def variant_count(self, obj):
        return obj.variants.count()

    variant_count.short_description = "Variants"


@admin.register(ProductVariant)
class ProductVariantAdmin(AdminImagePreviewMixin, admin.ModelAdmin):
    list_display = ["product", "sku", "price", "stock_quantity", "preview_image"]
    list_filter = ["product__product_type", "created_at"]
    search_fields = ["sku", "product__title"]
    autocomplete_fields = ["product"]
    readonly_fields = ["preview_image"]

    fieldsets = (
        (None, {"fields": ("product", "sku", "stock_quantity")}),
        ("Pricing", {"fields": (("price", "compare_at_price"),)}),
        ("Details", {"fields": ("attributes", ("image", "preview_image"))}),
    )

    formfield_overrides = {
        models.JSONField: {
            "widget": PrettyJSONWidget(
                attrs={"style": "width: 100%; height: 150px; font-family: monospace;"}
            )
        },
    }


@admin.register(ProductGalleryImage)
class ProductGalleryImageAdmin(AdminImagePreviewMixin, admin.ModelAdmin):
    list_display = ["product", "variant", "is_feature", "preview_image"]
    list_filter = ["is_feature"]
    autocomplete_fields = ["product", "variant"]
