import os
import django
import json
from datetime import datetime, timezone

# ВАЖНО: проверь имя модуля настроек! Если не config.settings — поменяй на своё.
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
        created_at = prod.created_at.isoformat() if prod.created_at else datetime.now(timezone.utc).isoformat()
        updated_at = prod.updated_at.isoformat() if prod.updated_at else datetime.now(timezone.utc).isoformat()

        fields = {
            "name": prod.name,
            "description": prod.description,
            "category": prod.category_id,
            "price": float(prod.price),
            "created_at": created_at,
            "updated_at": updated_at,
        }

        data.append({
            "model": "catalog.product",
            "pk": prod.pk,
            "fields": fields,
        })

    os.makedirs('fixtures', exist_ok=True)
    file_path = os.path.join('fixtures', 'shop_data.json')

    # Чистый UTF-8 без BOM — обязательно с двоеточием после with
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Фикстура сохранена. Объектов: {len(data)}")

if __name__ == '__main__':
    create_fixture()
