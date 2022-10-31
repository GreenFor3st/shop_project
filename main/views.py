from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'templates/index.html')

def store(request):
    return render(request, 'templates/store.html')
