from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        try:
            self.user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(f'The user with username {username} does not exist!')

        if not self.user.check_password(password):
            raise forms.ValidationError(f'Password for user {username} is not correct')


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-input'

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(widget=forms.PasswordInput())

    def set_request(self, request):
        self.request = request

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        user = authenticate(username=self.request.user.username, password=current_password)
        if not user:
            raise forms.ValidationError('The current password is incorrect.')
        return current_password

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']
        if new_password != confirm_new_password:
            raise forms.ValidationError('The new passwords do not match.')
        return confirm_new_password

    def save(self, user):
        new_password = self.cleaned_data['new_password']
        user.set_password(new_password)
        user.save()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
