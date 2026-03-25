from django.contrib import admin
from django.utils.html import format_html
from .models import ShopOwnerProfile


@admin.register(ShopOwnerProfile)
class ShopOwnerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'shop_name',
        'phone',
        'qr_token',
        'subscription_link',
        'created_at',
    )
    search_fields = ('user__username', 'shop_name', 'phone')
    readonly_fields = ('qr_token', 'created_at', 'subscription_link')

    def subscription_link(self, obj):
        return format_html(
            '<a href="http://127.0.0.1:8000/subscribe/{}/" target="_blank">Open Link</a>',
            obj.qr_token
        )

    subscription_link.short_description = 'QR Link'