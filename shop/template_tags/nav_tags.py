from django import template
from shop.models import Product, Category, Payment
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

