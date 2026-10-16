from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержимое')
    preview_image = models.ImageField('Превью', upload_to='blog_previews/', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_published = models.BooleanField('Опубликовано', default=False)
    views_count = models.PositiveIntegerField('Количество просмотров', default=0)

    class Meta:
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'
        ordering = ['-created_at']  # сначала новые записи

    def __str__(self):
        return self.title
