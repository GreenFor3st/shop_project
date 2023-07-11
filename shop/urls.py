from django.urls import path
from django.views.generic import TemplateView

from shop import views
from shop.views import show_category

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='store'),

    path('/cart_view/', views.CartView.as_view(), name='cart_view'),
    path('/category/<int:cat_id>/', show_category, name='category'),
    path('/detail/<int:pk>/', views.ProductsDetailView.as_view(), name='product'),
    path('/add-item-to-cart/<int:pk>', views.add_item_to_cart, name='add_item_to_cart'),

    path('/delete_item/<int:pk>', views.CartDeleteItem.as_view(), name='cart_delete_item'),
    path('/make-order/', views.make_order, name='make_order'),

    path('/payment/', views.PaymentView.as_view(), name='payment'),
    path('/make-payment/', views.make_payment, name='make_payment'),

]
