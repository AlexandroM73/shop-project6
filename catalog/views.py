from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from .models import Product

# Главная страница (можно оставить FBV, как у тебя)
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

# Детальная страница товара (уже был CBV — оставляем)
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

# Страница контактов — делаем на TemplateView
class ContactsView(TemplateView):
    template_name = 'contacts.html'
