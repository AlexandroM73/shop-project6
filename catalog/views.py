from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Product, Category  # не забудь импорт Category, если его нет
from .forms import ProductForm
from .services import get_products_by_category


# --- Главная страница (FBV) ---
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


# --- Список товаров ---
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10


# --- Детальная страница товара (теперь с кэшем страницы И передачей прав) ---
@method_decorator(cache_page(60 * 15), name='dispatch')  # 15 минут
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        user = self.request.user

        # Вычисляем права один раз здесь, в view
        is_owner = product.owner == user
        has_delete_perm = user.has_perm('catalog.delete_product')
        has_unpublish_perm = user.has_perm('catalog.can_unpublish_product')

        # Учитываем суперпользователя (он может всё)
        can_delete = is_owner or has_delete_perm or user.is_superuser
        can_unpublish = has_unpublish_perm or user.is_superuser

        context.update({
            'can_delete': can_delete,
            'can_unpublish': can_unpublish,
        })
        return context


# --- Страница контактов ---
class ContactsView(TemplateView):
    template_name = 'contacts.html'


# --- Товары категории (с низкоуровневым кэшем списка) ---
def category_products_list(request, category_id):
    products = get_products_by_category(category_id)
    category = get_object_or_404(Category, pk=category_id)

    return render(request, 'catalog/category_products.html', {
        'category': category,
        'products': products,
    })


# --- Создание товара (Задание 2: авто-привязка владельца) ---
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# --- Редактирование товара (Задание 2: только владелец) ---
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user and not request.user.is_superuser:
            raise Http404("Вы не можете редактировать этот товар")
        return super().dispatch(request, *args, **kwargs)


# --- Удаление товара (Задание 1 и 2: владелец ИЛИ модератор) ---
class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        is_owner = product.owner == user
        has_delete_perm = user.has_perm('catalog.delete_product')

        return is_owner or has_delete_perm or user.is_superuser


# --- Снятие с публикации (Задание 1: только модераторы) ---
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = Product.STATUS_DRAFT
    product.save()
    return redirect('product_detail', pk=product.pk)
