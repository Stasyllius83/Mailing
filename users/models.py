from django.db import models
from django.contrib.auth.models import AbstractUser

from mailing.models import NULLABLE

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)

    email_verify = models.BooleanField(default=False, verbose_name='почта проверена')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
