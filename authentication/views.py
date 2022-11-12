from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from authentication.forms import LoginForm


# Create your views here.
def login_user(request):
    context = {'Login_form': LoginForm()}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')

    return render(request, 'templates/auth/login.html', context)

def register_user(request):
    return render(request, 'templates/auth/register.html')

def logout_user(request):
    logout(request)
    return redirect('index')