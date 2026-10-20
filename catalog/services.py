import json
from django.core.cache import cache
from .models import Product

CACHE_TIMEOUT = 60 * 5  # 5 минут


def get_products_by_category(category_id):
    cache_key = f'category_{category_id}'

    # 1. Пытаемся получить из кэша
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        products = json.loads(cached_data)
        print(f"[CACHE HIT] category_{category_id}")
        return products

    print(f"[CACHE MISS] category_{category_id}")

    # 2. Запрос к БД
    qs = Product.objects.filter(
        category_id=category_id,
        status=Product.STATUS_PUBLISHED
    )

    # Превращаем в список словарей с правильными типами
    products = []
    for p in qs:
        # Цена: Decimal -> строка
        price_str = str(p.price) if p.price is not None else "0.00"

        # Картинка: ImageFieldFile -> URL (строка) или None
        image_url = None
        if p.image:
            image_url = p.image.url

        products.append({
            "id": p.id,
            "name": p.name,
            "price": price_str,
            "image": image_url,
            "category_id": p.category_id,
        })

    # 3. Сохраняем в кэш как JSON-строку
    cache.set(cache_key, json.dumps(products), timeout=CACHE_TIMEOUT)
    return products
