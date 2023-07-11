from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View

from authentication.forms import LoginForm, RegisterForm, ProfileForm, ChangePasswordForm


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
            else:
                context = {
                    'login_form': login_form,
                    'attention': f'this username {username} is not found!'
                }
        else:
            context = {
                'login_form': login_form,
            }
    return render(request, 'templates/auth/login.html', context)


class RegisterView(TemplateView):
    template_name = 'templates/auth/register.html'

    def get(self, request):
        user_form = RegisterForm()
        context = {'user_form': user_form}
        return render(request, 'templates/auth/register.html', context)

    def post(self, request):
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('index')

        context = {'user_form': user_form}
        return render(request, 'templates/auth/register.html', context)


class EditProfileView(LoginRequiredMixin, View):
    template_name = 'templates/auth/profile.html'
    login_url = 'login'

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            user_form = ProfileForm(instance=user)
        else:
            user_form = ProfileForm()
        context = {'user_form': user_form}
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            user_form = ProfileForm(request.POST, instance=user)
        else:
            user_form = ProfileForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
        context = {'user_form': user_form}
        return render(request, self.template_name, context)


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        form.set_request(request)
        if form.is_valid():
            form.save(request.user)
            return redirect('edit_profile')
    else:
        form = ChangePasswordForm()

    context = {'form': form}
    return render(request, 'templates/auth/change_password.html', context)


def logout_user(request):
    logout(request)
    return redirect('index')


