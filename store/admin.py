from django.contrib import admin
from .models import (
    Product,
    Variation,
    ProductAttribute,
    ReviewRating,
    Wishlist,
)


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


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'sku',
        'stock',
    )
    search_fields = ('product__product_name', 'sku')
    filter_horizontal = ('variations',)


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'product',
        'user',
        'rating',
        'status',
        'created_at',
    )
    list_filter = (
        'status',
        'rating',
        'created_at',
    )
    search_fields = (
        'subject',
        'review',
        'user__username',
        'product__product_name',
    )
    readonly_fields = ('ip', 'created_at', 'updated_at')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    search_fields = ('user__username', 'product__product_name')