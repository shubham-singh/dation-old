from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
# Register your models here.
from .models import *

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    exclude = ['user']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    exclude = ['user']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


class AutomaticallySaveUser(admin.ModelAdmin):
    exclude = ['user']
    # list_display = ('name', 'phone')
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

admin.site.register(Customer, AutomaticallySaveUser)
admin.site.register(Product, AutomaticallySaveUser)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, AutomaticallySaveUser)
admin.site.register(User, UserAdmin)