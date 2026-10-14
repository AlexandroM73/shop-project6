import os
import django
import json

# Инициализация Django (чтобы работали модели)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import Category, Product

def create_fixture():
    data = []

    # Категории
    for cat in Category.objects.all():
        data.append({
            "model": "catalog.category",
            "pk": cat.pk,
            "fields": {
                "name": cat.name,
                "description": cat.description,
            }
        })

    # Продукты
    for prod in Product.objects.all():
        data.append({
            "model": "catalog.product",
            "pk": prod.pk,
            "fields": {
                "name": prod.name,
                "description": prod.description,
                "image": prod.image.name if prod.image else None,
                "category": prod.category_id,
                "price": str(prod.price),
                "created_at": prod.created_at.isoformat(),
                "updated_at": prod.updated_at.isoformat(),
            }
        })

    with open('fixtures/shop_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Фикстура сохранена. Всего объектов: {len(data)}")

if __name__ == '__main__':
    create_fixture()
