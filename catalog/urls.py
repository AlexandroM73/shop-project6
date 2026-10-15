from django.urls import path
from .views import index, ProductDetailView, ContactsView

urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]
