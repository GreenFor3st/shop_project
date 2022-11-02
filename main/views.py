from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'templates/index.html')

def store(request):
    return render(request, 'templates/store.html')

def blank(request):
    return render(request, 'templates/blank.html')

def product(request):
    return render(request, 'templates/product.html')

def checkout(request):
    return render(request, 'templates/checkout.html')
