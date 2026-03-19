from django.contrib import admin
from .models import Product, Variation, ProductAttribute, Subscriber


# PRODUCT ADMIN
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name',
        'price',
        'category',
        'is_available',
        'modified_date',
    )
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ('is_available', 'category')
    search_fields = ('product_name', 'description')


# VARIATION ADMIN
@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'variation_category',
        'variation_value',
        'color_code',
        'is_active',
    )
    list_filter = ('variation_category', 'is_active')
    search_fields = ('product__product_name', 'variation_value')


# ⭐ SKU / STOCK ADMIN
@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'sku',
        'stock',
    )
    search_fields = ('product__product_name', 'sku')
    filter_horizontal = ('variations',)   # 👈 very important for usability


# ⭐ SUBSCRIBER ADMIN (YOUR ASSIGNMENT)
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        'phone_number',
        'birth_month',
        'created_at',
    )
    search_fields = ('phone_number', 'birth_month')
    list_filter = ('birth_month',)