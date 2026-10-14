from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from datetime import datetime, timezone

class Command(BaseCommand):
    help = 'Загружает тестовые данные (категории и товары) в базу данных'

    def handle(self, *args, **options):
        self.stdout.write('Очистка тестовых данных...')
        Category.objects.filter(name__in=['Электроника', 'Одежда']).delete()
        Product.objects.filter(name__in=['Смартфон X', 'Футболка базовая']).delete()

        self.stdout.write('Создание категорий...')
        cat_electronics = Category.objects.create(
            name='Электроника',
            description='Телефоны, ноутбуки, гаджеты'
        )
        cat_clothes = Category.objects.create(
            name='Одежда',
            description='Футболки, джинсы, аксессуары'
        )

        now = datetime.now(timezone.utc)

        self.stdout.write('Создание товаров...')
        Product.objects.create(
            name='Смартфон X',
            description='Хороший смартфон с отличной камерой',
            category=cat_electronics,
            price=299.99,
            created_at=now,
            updated_at=now
        )
        Product.objects.create(
            name='Футболка базовая',
            description='Белая футболка из 100% хлопка',
            category=cat_clothes,
            price=19.99,
            created_at=now,
            updated_at=now
        )

        count_cat = Category.objects.filter(name__in=['Электроника', 'Одежда']).count()
        count_prod = Product.objects.filter(name__in=['Смартфон X', 'Футболка базовая']).count()

        self.stdout.write(
            self.style.SUCCESS(f'Готово! Создано категорий: {count_cat}, товаров: {count_prod}')
        )
