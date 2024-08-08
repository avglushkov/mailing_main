from django.db import models
from users.models import User

# Create your models here.

class Blog(models.Model):

    header = models.CharField(max_length=255, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='blog/',blank=True, null=True, verbose_name='Изображение')
    count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.CharField(blank=True, null=True, max_length=100, verbose_name='Ссылка')
    published = models.BooleanField(default=True, verbose_name='Признак публикации')


    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


