import uuid

from django.db import models

from common.models import OrderableModel, TimestampedModel


def hero_section_upload_to(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"hero-sections/{uuid.uuid4()}.{ext}"


def featured_product_upload_to(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"featured-products/{uuid.uuid4()}.{ext}"


# Create your models here.
class FeaturedProduct(TimestampedModel, OrderableModel):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=featured_product_upload_to, null=True, blank=True
    )
