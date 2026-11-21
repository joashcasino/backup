from datetime import date, timedelta

from django.test import TestCase
from django.utils import timezone

from accounts.models import User

from .models import Item, LostReport


class ItemTests(TestCase):
    def test_overdue_when_with_finder_past_deadline(self):
        item = Item.objects.create(description="ID or card", place_found="CASS lobby", date_found=date.today())
        Item.objects.filter(pk=item.pk).update(created_at=timezone.now() - timedelta(days=5))
        item.refresh_from_db()
        self.assertTrue(item.is_overdue)

    def test_not_overdue_once_surrendered(self):
        item = Item.objects.create(
            description="Umbrella", place_found="Gym", date_found=date.today(), status=Item.Status.AVAILABLE,
        )
        Item.objects.filter(pk=item.pk).update(created_at=timezone.now() - timedelta(days=5))
        item.refresh_from_db()
        self.assertFalse(item.is_overdue)


class LostReportTests(TestCase):
    def test_new_report_is_open(self):
        owner = User.objects.create_user(username="o", email="o@g.msuiit.edu.ph", password="x")
        report = LostReport.objects.create(
            owner=owner, description="Scientific calculator", place_lost="Library", date_lost=date.today(),
        )
        self.assertEqual(report.status, LostReport.Status.OPEN)
