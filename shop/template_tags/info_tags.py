from shop.forms import BillingForm
from shop.models import Payment, Order
from django import template

register = template.Library()


########## Balance ###########
@register.simple_tag
def balance_context(request):
    if request.user.is_authenticated:
        balance = Payment.get_balance(request.user)
    else:
        balance = 0
    return balance

