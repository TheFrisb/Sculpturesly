import uuid

from django.db import models
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from common.models import TimestampedModel
from django.utils.translation import gettext_lazy as _

from common.utils import get_unique_slug


def get_product_slug(product):
    if product is None:
        return "unassigned"
    return product.slug or slugify(product.title) or "product"


def product_image_upload_to(instance, filename):
    ext = filename.split(".")[-1].lower()
    slug_part = get_product_slug(instance)
    return f"products/{slug_part}/main/{uuid.uuid4()}.{ext}"


def product_gallery_upload_to(instance, filename):
    ext = filename.split(".")[-1].lower()
    slug_part = get_product_slug(instance.product)
    return f"products/{slug_part}/gallery/{uuid.uuid4()}.{ext}"


def variant_upload_to(instance, filename):
    ext = filename.split(".")[-1].lower()
    slug_part = get_product_slug(instance.product)
    return f"products/{slug_part}/variants/{uuid.uuid4()}.{ext}"


class Category(MPTTModel, TimestampedModel):
    """
    Hierarchical categories using MPTT for efficient tree queries.
    Categories can have parent-child relationships.
    """

    name = models.CharField(max_length=255, verbose_name=_("Category Name"))
    slug = models.SlugField(
        max_length=255, unique=True, blank=True, verbose_name=_("Slug")
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("Parent Category"),
    )
    description = models.TextField(blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = get_unique_slug(self.__class__, base_slug, self)
        super().save(*args, **kwargs)


class Collection(TimestampedModel):
    """
    Product collections for grouping (e.g., featured, seasonal).
    Collections can have multiple products, and products can be in multiple collections.
    """

    name = models.CharField(max_length=255, verbose_name=_("Collection Name"))
    slug = models.SlugField(
        max_length=255, unique=True, blank=True, verbose_name=_("Slug")
    )
    description = models.TextField(blank=True, verbose_name=_("Description"))
    products = models.ManyToManyField(
        "Product", related_name="collections", blank=True, verbose_name=_("Products")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = get_unique_slug(self.__class__, base_slug, self)
        super().save(*args, **kwargs)


# Create your models here.
class Product(TimestampedModel):
    class Status(models.TextChoices):
        DRAFT = (
            "DRAFT",
            _("Draft"),
        )
        ARCHIVED = (
            "ARCHIVED",
            _("Archived"),
        )
        PUBLISHED = "PUBLISHED", _("Published")

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.DRAFT
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to=product_image_upload_to)
    categories = models.ManyToManyField(
        Category, related_name="products", blank=True, verbose_name=_("Categories")
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = get_unique_slug(self.__class__, base_slug, self)
        super().save(*args, **kwargs)


class ProductVariant(TimestampedModel):
    sku = models.CharField(max_length=255)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=10)
    image = models.ImageField(upload_to=variant_upload_to)
    categories = models.ManyToManyField(
        Category, related_name="variants", blank=True, verbose_name=_("Categories")
    )  # Optional: if variants need separate categories


class ProductImage(TimestampedModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="gallery"
    )
    image = models.ImageField(upload_to=product_gallery_upload_to)
