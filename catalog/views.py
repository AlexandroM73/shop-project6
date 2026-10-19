from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from .models import Product
from .forms import ProductForm


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


# --- Детальная страница товара ---
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


# --- Страница контактов ---
class ContactsView(TemplateView):
    template_name = 'contacts.html'


# --- Создание товара (Задание 2: авто-привязка владельца) ---
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        # САМОЕ ВАЖНОЕ: автоматически ставим текущего пользователя владельцем
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
        # Разрешаем редактирование только владельцу или суперпользователю
        if self.object.owner != request.user and not request.user.is_superuser:
            raise Http404("Вы не можете редактировать этот товар")
        return super().dispatch(request, *args, **kwargs)


# --- Удаление товара (Задание 1 и 2: владелец ИЛИ модератор) ---
class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    # Эта функция проверяет права перед удалением
    def test_func(self):
        product = self.get_object()
        user = self.request.user

        is_owner = product.owner == user
        has_delete_perm = user.has_perm('catalog.delete_product')

        # Возвращаем True, если: владелец ИЛИ есть право на удаление (модератор) ИЛИ суперпользователь
        return is_owner or has_delete_perm or user.is_superuser


# --- Снятие с публикации (Задание 1: только модераторы) ---
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = Product.STATUS_DRAFT
    product.save()
    return redirect('product_detail', pk=product.pk)
