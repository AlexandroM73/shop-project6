from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

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
]
