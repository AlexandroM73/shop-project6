from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(_('наименование'), max_length=200)
    description = models.TextField(_('описание'), blank=True)

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('категории')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_('наименование'), max_length=200)
    description = models.TextField(_('описание'), blank=True)
    image = models.ImageField(_('изображение'), upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('категория')
    )
    price = models.DecimalField(_('цена за покупку'), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(_('дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('дата последнего изменения'), auto_now=True)

    class Meta:
        verbose_name = _('продукт')
        verbose_name_plural = _('продукты')

    def __str__(self):
        return f"{self.name} ({self.category.name})"
