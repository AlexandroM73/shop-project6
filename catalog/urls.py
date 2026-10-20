from django.urls import path
from .views import (
    index,
    ContactsView,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    unpublish_product,
    category_products_list,  # <-- ДОБАВЛЕНО: view для категории с кэшем
)

urlpatterns = [
    # FBV главная
    path('', index, name='index'),

    # CBV список товаров
    path('products/', ProductListView.as_view(), name='product_list'),

    # Детальная страница
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    # Контакты
    path('contacts/', ContactsView.as_view(), name='contacts'),

    # CRUD формы
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # Снятие с публикации (только для модераторов)
    path('product/<int:pk>/unpublish/', unpublish_product, name='unpublish_product'),

    # НОВАЯ СТРОКА: товары категории (с низкоуровневым кэшем)
    path('category/<int:category_id>/', category_products_list, name='category_products'),
]
