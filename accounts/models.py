from django.contrib.auth.models import AbstractUser

from common.models import TimestampedModel


# Create your models here.
class User(TimestampedModel, AbstractUser):
    pass
