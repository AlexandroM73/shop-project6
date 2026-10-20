from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings  # Важно: не импортируем модель пользователя напрямую

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Название"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    # --- Статусы публикации (Задание 1) ---
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_ARCHIVED = 'archived'

    STATUS_CHOICES = [
        (STATUS_DRAFT, _("Черновик")),
        (STATUS_PUBLISHED, _("Опубликован")),
        (STATUS_ARCHIVED, _("В архиве")),
    ]

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

    # --- Новое поле: статус публикации ---
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        help_text=_("Статус продукта: черновик, опубликован или в архиве."),
        verbose_name=_("Статус публикации")
    )

    # --- Новое поле: владелец продукта (Задание 2) ---
    # Используем settings.AUTH_USER_MODEL вместо прямого импорта CustomUser
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,  # null=True нужен, чтобы старые продукты не сломали миграцию
        blank=True,
        verbose_name=_("Владелец")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")
        ordering = ['-created_at']
        # --- Кастомные права (Задание 1) ---
        permissions = [
            ("can_unpublish_product", _("Может отменять публикацию продукта")),
        ]

    def __str__(self):
        status_display = self.get_status_display()
        owner_name = self.owner.email if self.owner else "Нет владельца"
        return f"{self.name} [{status_display}] (владелец: {owner_name})"
