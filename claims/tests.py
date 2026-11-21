import io
import shutil
import tempfile
from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from accounts.models import User
from items.models import Item

from .models import Claim
from .storage import private_storage


def tiny_png():
    buf = io.BytesIO()
    Image.new("RGB", (2, 2)).save(buf, format="PNG")
    return SimpleUploadedFile("proof.png", buf.getvalue(), content_type="image/png")


class ClaimTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Write test uploads to a temporary folder, not the real private_media/
        cls.tmp = tempfile.mkdtemp()
        cls._old = private_storage._location
        private_storage._location = cls.tmp
        for attr in ("base_location", "location"):
            private_storage.__dict__.pop(attr, None)

    @classmethod
    def tearDownClass(cls):
        private_storage._location = cls._old
        for attr in ("base_location", "location"):
            private_storage.__dict__.pop(attr, None)
        shutil.rmtree(cls.tmp, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.owner = User.objects.create_user(username="owner", email="owner@g.msuiit.edu.ph", password="x")
        self.other = User.objects.create_user(username="other", email="other@g.msuiit.edu.ph", password="x")
        self.sid = User.objects.create_user(
            username="sid", email="sid@g.msuiit.edu.ph", password="x", role=User.Role.SID,
        )
        self.item = Item.objects.create(
            description="Black backpack", place_found="Library entrance", date_found=date.today(),
            status=Item.Status.AVAILABLE,
        )
        self.claim = Claim.objects.create(
            item=self.item, claimant=self.owner, contents="Two notebooks", proof_photo=tiny_png(),
        )
        self.url = reverse("claims:proof_photo", args=[self.claim.pk])

    def test_claimant_and_sid_can_open_proof_photo(self):
        for user in (self.owner, self.sid):
            self.client.force_login(user)
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)
            response.close()

    def test_other_users_cannot_open_proof_photo(self):
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_proof_photo_is_not_under_public_media(self):
        with self.assertRaises(ValueError):
            self.claim.proof_photo.url  # no public URL on purpose
        self.assertTrue(self.claim.proof_photo.path.startswith(self.tmp))

    def test_only_one_pending_claim_per_user_per_item(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Claim.objects.create(item=self.item, claimant=self.owner, contents="again")

    def test_new_claim_allowed_after_withdrawing(self):
        self.claim.status = Claim.Status.WITHDRAWN
        self.claim.save()
        Claim.objects.create(item=self.item, claimant=self.owner, contents="again")
