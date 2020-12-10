from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('add-customer', views.add_customer, name='addCustomer'),
    path('add-product', views.add_product, name='addProduct'),
    path('order', views.order, name='order'),
    path('logout', views.logout_view, name='logout')   
]