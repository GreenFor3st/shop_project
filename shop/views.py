from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count

from django.views.generic import ListView, DetailView, DeleteView, TemplateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.urls import reverse_lazy

from shop.forms import AddQuantityForm, BillingForm
from shop.models import Product, Order, OrderItem


class ProductsListView(ListView):
    model = Product
    template_name = 'templates/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = list(set(Product.objects.values_list('category').annotate(category_count=Count('category'))))
        context['categories'] = categories
        return context


class ProductsDetailView(DetailView):
    model = Product
    template_name = 'templates/product.html'


@login_required(login_url=reverse_lazy('login'))
def add_item_to_cart(request, pk):
    if request.method == 'POST':
        quantity_form = AddQuantityForm(request.POST)
        if quantity_form.is_valid():
            quantity = quantity_form.cleaned_data['quantity']
            if quantity:
                cart = Order.get_cart(request.user)
                # product = Product.objects.get(pk=pk)
                product = get_object_or_404(Product, pk=pk)
                cart.orderitem_set.create(product=product,
                                          quantity=quantity,
                                          price=product.price)
                cart.save()
                return redirect('store')
        else:
            pass
    return redirect('store')


class CartView(ListView):
    model = Order
    template_name = 'templates/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Order.get_cart(self.request.user)
        items = cart.orderitem_set.all()
        form = BillingForm(instance=cart)

        context['cart'] = cart
        context['items'] = items
        context['form'] = form
        return context


@method_decorator(login_required, name='dispatch')
class CartDeleteItem(DeleteView):
    model = OrderItem
    template_name = 'shop/cart.html'
    success_url = reverse_lazy('cart_view')

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(order__user=self.request.user)
        return qs


@login_required(login_url=reverse_lazy('login'))
def make_order(request):
    if request.method == "POST":
        cart = Order.get_cart(request.user)
        form = BillingForm(request.POST, instance=cart)
        if form.is_valid():

            form.save()
            cart.make_order()
            return redirect('store')
    else:
        cart = Order.get_cart(request.user)
        form = BillingForm(instance=cart)

    return render(request, 'templates/cart.html', {'form': form})
