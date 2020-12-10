from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import *
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)



admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(User, UserAdmin)