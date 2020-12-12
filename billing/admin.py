from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import *
# Register your models here.

class FilterUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


class CustomerAdmin(FilterUserAdmin):
    exclude = ['user']
    list_display = ('name', 'phone')
    search_fields = ['name', 'phone']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    exclude = ['user', 'price']
    autocomplete_fields = ['product']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = Product.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class OrderItemAdmin(FilterUserAdmin):
    list_display = ('order_id', 'product', 'quantity', 'discount', 'price')

    def order_id(self, obj):
        return obj.order.orderid

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ['user']
        if not request.user.is_superuser:
            self.exclude.append('user')
        form = super(OrderItemAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['product'].queryset = Product.objects.filter(user=request.user)
        return form

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

class OrderAdmin(FilterUserAdmin):
    list_display = ('ordertype', 'orderid', 'customer', 'date')
    list_filter = ('ordertype',)
    search_fields = ['orderid', 'customer__name']
    autocomplete_fields = ['customer']
    inlines = [
        OrderItemInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ['user']
        if not request.user.is_superuser:
            self.exclude.append('user')
        form = super(OrderAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['customer'].queryset = Customer.objects.filter(user=request.user)
        return form
    
    def stock(quantity, Product):
        product = Product
        product = product.stock - quantity
        product.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.user = request.user
            instance.price = (instance.quantity * instance.product.price) - instance.discount
            if(instance.order.ordertype == 'B'):
                instance.product.stock = instance.product.stock + instance.quantity
                instance.product.save()
            else:
                instance.product.stock = instance.product.stock - instance.quantity
                instance.product.save()
            instance.save()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

class ProductAdmin(FilterUserAdmin):
    exclude = ['user']
    list_display = ('name', 'product_ID', 'price', 'stock')
    search_fields = ['name']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(User, UserAdmin)