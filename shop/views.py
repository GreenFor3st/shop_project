from django.shortcuts import render
from django.db.models import Count

from django.views.generic import ListView
from shop.models import Product


class ProductsListView(ListView):
    model = Product
    template_name = 'templates/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = list(set(Product.objects.values_list('category', flat=True)))
        context['categories'] = categories
        return context
