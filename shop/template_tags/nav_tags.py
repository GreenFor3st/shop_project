from django import template

from shop.forms import BillingForm
from shop.models import Product, Category, Payment, Order
from django.db.models import Count

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('templates/store/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        categories = Category.objects.annotate(product_count=Count('product'))
    else:
        categories = Category.objects.annotate(product_count=Count('product')).order_by(sort)

    return {"cats": categories, "cat_selected": cat_selected}


########## Cart wiget ###########
@register.inclusion_tag('templates/cart_widget.html')
def cart_context(request):
    cart = Order.get_cart(request.user)
    items = cart.orderitem_set.all()
    form = BillingForm(instance=cart)
    context = {
        'cart': cart,
        'items': items,
        'form': form,
    }
    return context
