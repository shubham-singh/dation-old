from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import *
from .models import *

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
          return render(request, "hello/login.html", {
                "message": "Invalid credentials"
            })
    return render(request, "hello/login.html")

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    customer_form = CustomerForm()
    
    product_form = ProductForm()
    
    order_form = OrderForm()
    order_form.fields['customer'].queryset = Customer.objects.filter(user=request.user)

    orderproduct = OrderProductFormSet()
    for f in orderproduct:
        f.fields['product'].queryset = Product.objects.filter(user=request.user)

    # orderproduct.empty_form.fields['product'].queryset = Product.objects.filter(user=request.user)


    return render(request, 'hello/home.html', {
        "customer_form": customer_form,
        'product_form': product_form,
        'order_form': order_form,
        'orderproduct_form': orderproduct
    })

def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            customer = form.cleaned_data.get('name')
            messages.success(request, "Customer Added: " + customer)
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.warning(request, 'No Customer Added')
    else:
        return HttpResponseRedirect(reverse('index'))

def order(request):
    # if request.method == 'POST':
    #     orderform = OrderForm(request.POST)
    #     if orderform.is_valid():
    #         orderform.save()
    #         orderitemform = OrderItemForm(request.POST)
    #         if orderitemform.is_valid():
    #             orderitemform.save()
    #             return HttpResponseRedirect(reverse('index'))
    # else:
    #     return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        order = OrderForm(request.POST)
        order.instance.user = request.user
        if order.is_valid():
            create_order = order.save(commit=False)
            products = OrderProductFormSet(request.POST, instance=create_order)
            for p in products:
                p.instance.user = request.user
            if products.is_valid():
                order.save()
                products.save()
                messages.success(request, 'Order Placed!')
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.warning(request, 'Failed to add products to Order :(')
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.warning(request, 'Order Failed :(')
            return HttpResponseRedirect(reverse('index'))
    
    else:
        return HttpResponseRedirect(reverse('index'))



def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            product = form.cleaned_data.get('name')
            messages.success(request, "Product Added: " + product)
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.warning(request, 'No product Added')
    else:
        return HttpResponseRedirect(reverse('index'))

def logout_view(request):
    logout(request)
    # return render(request, "hello/login.html", {
    #             "message": "Logged out successfully"
    #         })
    return HttpResponseRedirect(reverse('index'))