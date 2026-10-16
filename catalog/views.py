from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm  # <-- важно: импортируем форму с валидацией и стилями

# Главная страница (FBV оставляем, как у тебя)
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

# Список товаров (ListView) — нужен для CRUD
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'  # убедись, что шаблон лежит в catalog/templates/catalog/
    context_object_name = 'products'
    paginate_by = 10

# Детальная страница товара (CBV)
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

# Страница контактов (TemplateView)
class ContactsView(TemplateView):
    template_name = 'contacts.html'

# Создание товара (CreateView)
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

# Редактирование товара (UpdateView)
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

# Удаление товара (DeleteView)
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
