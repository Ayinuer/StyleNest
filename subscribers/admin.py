from django.contrib import admin
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('masked_phone_number', 'shop', 'birth_month', 'is_active', 'created_at')
    list_filter = ('birth_month', 'is_active', 'shop')
    search_fields = ('encrypted_phone_number',)

    def masked_phone_number(self, obj):
        phone = obj.get_phone_number()
        if len(phone) >= 4:
            return f"****{phone[-4:]}"
        return "Hidden"

    masked_phone_number.short_description = "Phone Number"