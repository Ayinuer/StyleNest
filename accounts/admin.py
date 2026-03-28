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
        'open_link',
        'created_at',
    )
    search_fields = ('shop_name', 'user__username', 'qr_token')
    readonly_fields = ('qr_token', 'qr_code', 'created_at')

    def open_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank">Open Link</a>',
            obj.get_subscribe_url()
        )

    open_link.short_description = 'QR Link'