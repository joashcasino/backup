from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from items.models import Item

from .storage import get_private_storage


class Claim(models.Model):
    """An owner's claim on a found item (US-07), reviewed by SID (US-11), released (US-17)."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved – awaiting pickup"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"      # claimant withdrew while Pending
        CANCELLED = "cancelled", "Cancelled"      # claimant cancelled after approval, or approval expired
        PICKED_UP = "picked_up", "Picked up"      # SID recorded the release

    class IdType(models.TextChoices):
        SCHOOL_ID = "school_id", "School ID"
        GOVERNMENT_ID = "government_id", "Other government ID"

    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="claims")
    claimant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="claims",
    )

    # Claimant's answers. Visible to the claimant and SID only.
    color = models.CharField(max_length=50, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    contents = models.TextField()
    marks = models.TextField("marks or attachments", blank=True)
    date_lost_from = models.DateField(null=True, blank=True)
    date_lost_to = models.DateField(null=True, blank=True)
    place_lost = models.CharField(max_length=255, blank=True)
    proof_photo = models.ImageField(upload_to="claims/", storage=get_private_storage, blank=True)

    # SID review (US-11)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    rejection_reason = models.TextField(blank=True)  # required when rejecting; shown to the claimant
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="reviewed_claims",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    pickup_deadline = models.DateField(null=True, blank=True)

    # Release record (US-17)
    id_type_checked = models.CharField(max_length=20, choices=IdType.choices, blank=True)
    released_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="released_claims",
    )
    released_at = models.DateTimeField(null=True, blank=True)

    hidden_by_claimant = models.BooleanField(default=False)  # "Remove from list" in My claims
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["item", "claimant"],
                condition=models.Q(status="pending"),
                name="one_pending_claim_per_user_per_item",
            ),
            models.CheckConstraint(
                condition=models.Q(date_lost_from__isnull=True)
                | models.Q(date_lost_to__isnull=True)
                | models.Q(date_lost_from__lte=models.F("date_lost_to")),
                name="claim_date_range_in_order",
            ),
        ]

    def __str__(self):
        return f"{self.item} · {self.claimant} ({self.get_status_display()})"

    def can_view(self, user):
        """Only the claimant and SID staff may see the answers and proof photo."""
        return user.is_authenticated and (user.pk == self.claimant_id or user.is_sid)

    def default_pickup_deadline(self):
        return timezone.localdate() + timedelta(days=settings.PICKUP_DEADLINE_DAYS)
