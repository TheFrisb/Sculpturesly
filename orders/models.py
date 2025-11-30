import secrets
import string
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from common.models import TimestampedModel
from products.models import ProductVariant


class OrderAddress(TimestampedModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(_("Email Address"))
    phone = models.CharField(_("Phone Number"), max_length=50, blank=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country = CountryField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}"


class Order(TimestampedModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PAID = "PAID", _("Paid")
        PROCESSING = "PROCESSING", _("Processing")
        SHIPPED = "SHIPPED", _("Shipped")
        DELIVERED = "DELIVERED", _("Delivered")
        CANCELLED = "CANCELLED", _("Cancelled")
        REFUNDED = "REFUNDED", _("Refunded")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    email = models.EmailField(_("Customer Email"))
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_address = models.ForeignKey(
        OrderAddress, related_name="shipping_orders", on_delete=models.PROTECT
    )
    billing_address = models.ForeignKey(
        OrderAddress,
        related_name="billing_orders",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    stripe_payment_intent_id = models.CharField(
        max_length=255, blank=True, db_index=True
    )
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.order_number} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.order_number:
            timestamp = timezone.now().strftime("%y%m%d")

            alphabet = string.ascii_uppercase + string.digits
            random_suffix = "".join(secrets.choice(alphabet) for _ in range(4))
            self.order_number = f"ORD-{timestamp}-{random_suffix}"

        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_lines",
    )
    product_sku = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    attributes = models.JSONField(default=dict)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    def save(self, *args, **kwargs):
        if not self.total_price and self.unit_price and self.quantity:
            self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
