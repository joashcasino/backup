from django.conf import settings
from django.db import models


class Item(models.Model):
    class Status(models.TextChoices):
        WITH_FINDER = "with_finder", "With finder"
        AVAILABLE = "available", "Available"
        CLAIM_PENDING = "claim_pending", "Claim pending"
        APPROVED = "approved", "Approved – awaiting pickup"
        CLAIMED = "claimed", "Claimed"

    class Category(models.TextChoices):
        ID_CARD = "id_card", "ID or card"
        WALLET = "wallet", "Wallet"
        BAG = "bag", "Bag"
        ELECTRONICS = "electronics", "Electronics"
        CLOTHING = "clothing", "Clothing"
        OTHER = "other", "Other"

    # Public details (shown on listings)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    place_found = models.CharField(max_length=255)
    date_found = models.DateField()
    photo = models.ImageField(upload_to="items/", blank=True)  # public (blurred) copy only
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.WITH_FINDER)

    # Who posted it
    finder = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="found_items",
    )

    # Filled in when SID logs the item (US-09)
    item_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    finder_name = models.CharField(max_length=150, blank=True)
    condition_note = models.TextField(blank=True)
    holder = models.CharField(max_length=100, blank=True)          # e.g. "SID Office"
    claim_location = models.CharField(max_length=255, blank=True)  # e.g. "Admin Building, Room 101"
    logged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="logged_items",
    )
    logged_at = models.DateTimeField(null=True, blank=True)

    # SID-ONLY. Never show this on any public template (NFR-01, NFR-02).
    hidden_verification_detail = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_found", "-created_at"]

    def __str__(self):
        return f"{self.description} ({self.get_status_display()})"