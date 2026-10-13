from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Название"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ['name']  # Сортировка по умолчанию

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Название"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name=_("Изображение")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_("Категория")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Цена")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")
        ordering = ['-created_at']  # Новые товары сверху

    def __str__(self):
        return f"{self.name} ({self.category.name})"
