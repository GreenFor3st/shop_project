from django.urls import path
from django.views.generic import TemplateView

from shop import views

urlpatterns = [
    # path('fill-database/', views.fill_database, name='fill_database'),
    path('', views.ProductsListView.as_view(), name='store'),
    path('cart_view/', TemplateView.as_view(template_name='cart.html'), name='cart_view'),
    path('detail/<int:pk>/',TemplateView.as_view(template_name='product.html'), name='product')
]