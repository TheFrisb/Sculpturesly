from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimestampedModel
from products.models import ProductVariant


# Create your models here.
class Cart(TimestampedModel):
    class Status(models.TextChoices):
        ABANDONED = "ABANDONED", _("Abandoned")
        ACTIVE = "ACTIVE", _("Active")

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    session_key = models.CharField(max_length=255, db_index=True)


class CartItem(TimestampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
