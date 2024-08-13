from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    birthdate = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
