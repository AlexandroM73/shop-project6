import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from catalog.models import Category, Product
from django.contrib.auth import get_user_model

User = get_user_model()

print("--- Начало генерации тестовых данных ---")

# 1. Категория
if Category.objects.count() == 0:
    cat = Category.objects.create(name="Тестовая категория", slug="test-cat")
    print(f"✅ Создана категория: ID={cat.id}")
else:
    cat = Category.objects.first()
    print(f"📂 Найдена категория: ID={cat.id}, name='{cat.name}'")

# 2. Пользователь
if User.objects.count() == 0:
    user = User.objects.create_user(username='testuser', password='12345')
    print(f"👤 Создан пользователь: {user.username}")
else:
    user = User.objects.first()
    print(f"👤 Используется пользователь: {user.username}")

# 3. Товар
if Product.objects.filter(category_id=cat.id).count() == 0:
    prod = Product.objects.create(
        name="Тестовый товар для кэша",
        price=1990,
        category=cat,
        owner=user,
        status=Product.STATUS_PUBLISHED
    )
    print(f"🛒 Создан товар: '{prod.name}', категория ID={prod.category_id}")
else:
    print("📦 В этой категории уже есть товары, пропускаем создание.")

# 4. Проверка
print("\n📋 Список всех товаров в базе:")
for p in Product.objects.all():
    print(f"- '{p.name}' | Категория ID: {p.category_id} | Статус: {p.status}")

print("--- Готово ---")
