from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin


# Create your models here.
def get_sentinel_customer():
    return Customer.objects.get_or_create(name='deleted_customer')[0]

def get_sentinel_product():
    return Product.objects.get_or_create(name='deleted_product', price=0)[0]

class User(AbstractUser):
    pass
class Customer(models.Model):
    name = models.CharField(max_length=70)
    phone = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    name = models.CharField(max_length=70)
    product_ID = models.CharField(max_length=14)
    price = models.FloatField()
    stock = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product")

    def __str__(self):
        return f"{self.product_ID}: {self.name}"

class Order(models.Model):
    BUY = 'B'
    SELL = 'S'
    ORDER_TYPE = [
        (BUY, 'BUY'),
        (SELL, 'SELL')
    ]
    ordertype = models.CharField(max_length=1, choices=ORDER_TYPE)
    orderid = models.CharField(max_length=21, unique=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    customer = models.ForeignKey(Customer, on_delete=models.SET(get_sentinel_customer), null=True)
    date = models.DateField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")

    def _str__(self):
        return f"{self.orderid}: {order.who}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET(get_sentinel_product))
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    discount = models.FloatField(default=0)
    price = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orderitem")