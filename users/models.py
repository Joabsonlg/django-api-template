from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.is_active = True
        super().save(*args, **kwargs)
