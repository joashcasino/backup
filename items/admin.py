from django.contrib import admin

from .models import Item, LostReport


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("description", "category", "status", "date_found", "item_code")
    list_filter = ("status", "category")
    search_fields = ("description", "item_code", "finder_name")


@admin.register(LostReport)
class LostReportAdmin(admin.ModelAdmin):
    list_display = ("description", "owner", "place_lost", "date_lost", "status")
    list_filter = ("status", "category")
    search_fields = ("description", "place_lost", "owner__email")
