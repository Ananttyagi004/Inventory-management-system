from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'description', 'created_at', 'updated_at']
    search_fields = ['sku', 'name']
    ordering = ['sku']
