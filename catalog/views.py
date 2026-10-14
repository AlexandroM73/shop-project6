from django.shortcuts import render
from django.views.generic import DetailView
from .models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})
