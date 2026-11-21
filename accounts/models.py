from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        MEMBER = "member", "Owner / Finder"
        SID = "sid", "SID staff"

    # Google sign-in matches accounts by email, so each email can belong to one user only.
    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

    @property
    def is_sid(self):
        return self.role == self.Role.SID
