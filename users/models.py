from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['id']