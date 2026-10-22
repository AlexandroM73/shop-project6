from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Важно: используем email для авторизации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # password всё равно обязателен, но email — ключ

    def __str__(self):
        return self.email
