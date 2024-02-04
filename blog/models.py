
from django.db import models
from django.urls import reverse
from config import settings
from mailing.models import NULLABLE

class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    slug = models.SlugField(max_length=255, unique=True, **NULLABLE, verbose_name='URL')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Автор', **NULLABLE)
    content = models.TextField(verbose_name='содержимое', **NULLABLE)
    preview = models.ImageField(upload_to='blog/static/img/', verbose_name='изображение', **NULLABLE)
    date_create = models.DateTimeField(verbose_name='дата создания', **NULLABLE)
    is_published = models.BooleanField(default=True, verbose_name='признак публикации')
    count_views = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ('count_views',)


    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})
