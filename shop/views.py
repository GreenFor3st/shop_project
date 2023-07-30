from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import ListView, DetailView, DeleteView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.urls import reverse_lazy

from shop.forms import AddQuantityForm, BillingForm, PaymentForm
from shop.models import Product, Order, OrderItem, Category, Payment


class ProductsListView(ListView):
    model = Product
    template_name = 'templates/store/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = 0
        return context


def show_category(request, cat_id):
    cat_selected = Category.objects.filter(pk=cat_id)
    products = Product.objects.filter(cat__in=cat_selected)
    return render(request, 'templates/store/store.html', {'object_list': products, 'cat_selected': cat_id})


class ProductsDetailView(DetailView):
    model = Product
    template_name = 'templates/store/product.html'


@login_required(login_url=reverse_lazy('login'))
def add_item_to_cart(request, pk):
    if request.method == 'POST':
        quantity_form = AddQuantityForm(request.POST)
        if quantity_form.is_valid():
            quantity = quantity_form.cleaned_data['quantity']
            if quantity:
                cart = Order.get_cart(request.user)
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
    template_name = 'templates/store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Order.get_cart(self.request.user)
        items = cart.orderitem_set.all()
        form = BillingForm(instance=cart)

        context['cart'] = cart
        context['items'] = items
        context['form'] = form
        return context


class PaymentView(ListView):
    model = Payment
    template_name = 'templates/store/payment.html'


@login_required(login_url=reverse_lazy('login'))
def make_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        print(form)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            print(amount)
            Payment.objects.create(user=request.user, amount=amount)
            return redirect('store')

    context = {'form': form}
    return render(request, 'templates/store/payment.html', context)


@method_decorator(login_required, name='dispatch')
class CartDeleteItem(DeleteView):
    model = OrderItem
    template_name = 'templates/store/cart.html'

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(order__user=self.request.user)
        return qs


@login_required(login_url=reverse_lazy('login'))
def make_order(request):
    cart = Order.get_cart(request.user)
    items = cart.orderitem_set.all()
    if request.method == "POST":
        cart = Order.get_cart(request.user)
        form = BillingForm(request.POST, instance=cart)
        if form.is_valid():
            form.save()
            cart.make_order()
            return redirect('store')

    context = {'form': form, 'cart': cart, 'items': items}

    return render(request, 'templates/store/cart.html', context)
