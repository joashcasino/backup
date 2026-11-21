from django.contrib import admin

from .models import Claim


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ("item", "claimant", "status", "created_at", "reviewed_by", "released_at")
    list_filter = ("status",)
    search_fields = ("item__description", "item__item_code", "claimant__email")
    raw_id_fields = ("item", "claimant", "reviewed_by", "released_by")
