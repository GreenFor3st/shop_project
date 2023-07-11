from _decimal import Decimal

from django import forms

from shop.models import OrderItem, Order, Product, Payment


class AddQuantityForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['min'] = 1


class BillingForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'country', 'zip_code', 'tel']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['address'].required = True
        self.fields['city'].required = True
        self.fields['country'].required = True
        self.fields['zip_code'].required = True
        self.fields['tel'].required = True


class PaymentForm(forms.ModelForm):
    amount = forms.DecimalField(decimal_places=2, max_digits=20)

    class Meta:
        model = Payment
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].required = True

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        try:
            decimal_amount = Decimal(amount)
        except (ValueError, TypeError) as e:
            print(e)
            raise forms.ValidationError("Value must be a decimal number.")
        if decimal_amount < 10:
            raise forms.ValidationError("The amount must be greater than 10$.")
        if decimal_amount is not int:
            raise forms.ValidationError("Only integer numbers.")

        return decimal_amount


