from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name='телефон')
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='страна')
    avatar = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name='аватар')

    code = models.CharField(max_length=100, blank=True, null=True, verbose_name='токен')

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [("can_deactivate_user", "Can deactivate user",)]

    def __str__(self):
        return self.email


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []