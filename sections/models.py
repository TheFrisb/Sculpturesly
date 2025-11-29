import uuid

from django.db import models

from common.models import OrderableModel, TimestampedModel


def hero_section_upload_to(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"hero-sections/{uuid.uuid4()}.{ext}"


# Create your models here.
class HeroSection(TimestampedModel, OrderableModel):
    image = models.ImageField(upload_to=hero_section_upload_to)
    headline = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    primary_button_text = models.CharField(max_length=255)
    secondary_button_text = models.CharField(max_length=255)

    def __str__(self):
        return self.headline
