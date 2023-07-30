from django.shortcuts import render
from django.views.generic import ListView

from shop.models import Product


# Create your views here.
class IndexView(ListView):
    model = Product
    template_name = 'templates/index.html'


def store(request):
    return render(request, 'templates/store.html')


def blank(request):
    return render(request, 'templates/blank.html')


def product(request):
    return render(request, 'templates/product.html')


def checkout(request):
    return render(request, 'templates/cart.html')
