from django.contrib import admin
from .models import ShopOwner

@admin.register(ShopOwner)
class ShopOwnerAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user', 'phone_number', 'slug')
    prepopulated_fields = {'slug': ('shop_name',)}