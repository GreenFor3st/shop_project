from django import forms

from shop.models import OrderItem, Order


class AddQuantityForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']


class BillingForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'country', 'zip_code', 'tel']

        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.TextInput(),
            'address': forms.TextInput(),
            'city': forms.TextInput(),
            'country': forms.TextInput(),
            'zip_code': forms.TextInput(),
            'tel': forms.TextInput()
        }
