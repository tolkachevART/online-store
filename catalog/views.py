from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from catalog.forms import ProductForm
from catalog.models import Product


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/create_product.html'
    success_url = reverse_lazy('catalog:product_detail')
