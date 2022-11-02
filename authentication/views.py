from django.shortcuts import render

# Create your views here.
def login_user(request):
    return render(request, 'templates/auth/login.html')

def register_user(request):
    return render(request, 'templates/auth/register.html')

def logout_user(request):
    pass