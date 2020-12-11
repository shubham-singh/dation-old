from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class AuthenticationFormWithInactiveUsersOkay(AuthenticationForm):
    class Meta:
        model = User
    def confirm_login_allowed(self, user):
        pass

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['user']
        # fields = '__all__'

        widgets = {
            'name': forms.TextInput( attrs = {
                'class': 'form-control',
                'placeholder': "Customer's name",
                'autofocus': 'on'
                }),
            'phone': forms.TextInput( attrs = {
                'class': 'form-control',
                'placeholder': "Customer's phone number"
                }),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['user']
        # fields = '__all__'

        widgets = {
            'name': forms.TextInput( attrs = {
                'class': 'form-control',
                'placeholder': "Products's name",
                'autofocus': 'on'
                }),
            'product_ID': forms.TextInput( attrs = {
                'class': 'form-control',
                'placeholder': 'Product ID'
                }),
            'price': forms.TextInput( attrs = {
                'class': 'form-control',
                'placeholder': 'Product price'
                }),
            'stock': forms.TextInput( attrs = {
                'class': 'form-control',
                'placeholder': 'Stock'
                }),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['products', 'user', 'date']

OrderProductFormSet = forms.inlineformset_factory(Order, OrderItem, exclude=['user'], extra=1)