from django.db import models


# Create your models here.
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrderableModel(models.Model):
    sort_order = models.IntegerField(default=0, blank=False, null=True)

    class Meta:
        abstract = True
