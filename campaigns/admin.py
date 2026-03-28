from django.contrib import admin
from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'shop',
        'message_type',
        'template_type',
        'status',
        'total_recipients',
        'delivered_count',
        'failed_count',
        'created_at',
    )
    list_filter = ('message_type', 'template_type', 'status')
    search_fields = ('title', 'message_body', 'shop__shop_name')