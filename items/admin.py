from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("description", "category", "status", "date_found", "item_code")
    list_filter = ("status", "category")
    search_fields = ("description", "item_code")