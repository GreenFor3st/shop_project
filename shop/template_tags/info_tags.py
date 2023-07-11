from shop.models import Payment
from django import template

register = template.Library()


@register.simple_tag
def balance_context(request):
    if request.user.is_authenticated:
        balance = Payment.get_balance(request.user)
    else:
        balance = 0
    return balance

