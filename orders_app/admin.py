from django.contrib import admin
from .models import Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('product', 'quantity', 'product_price', 'created_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'full_name',
        'phone',
        'order_total',
        'grand_total',
        'status',
        'is_ordered',
        'created_at',
    )
    list_filter = ('status', 'is_ordered', 'created_at')
    search_fields = ('order_number', 'full_name', 'email', 'phone')
    readonly_fields = (
        'order_number',
        'order_total',
        'grand_total',
        'created_at',
        'updated_at',
    )
    inlines = [OrderProductInline]
    ordering = ('-created_at',)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity',
        'product_price',
        'ordered',
        'created_at',
    )
    list_filter = ('ordered', 'created_at')
    search_fields = ('product__product_name', 'order__order_number')
    ordering = ('-created_at',)