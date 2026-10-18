from django.urls import path
from . import views
from .views import ProductDetailView

urlpatterns = [
    path('', views.index, name='index'),                 # Главная: /
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Товар: /products/1/
]
