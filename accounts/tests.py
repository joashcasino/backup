from types import SimpleNamespace

from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from allauth.core.exceptions import ImmediateHttpResponse

from .adapters import SocialAccountAdapter, is_campus_email
from .models import User


def make_user(username, role=User.Role.MEMBER):
    return User.objects.create_user(
        username=username, email=f"{username}@g.msuiit.edu.ph", password="x", role=role,
    )


@override_settings(ALLOWED_EMAIL_DOMAIN="g.msuiit.edu.ph")
class CampusEmailTests(TestCase):
    def test_campus_email_rule(self):
        self.assertTrue(is_campus_email("juan.delacruz@g.msuiit.edu.ph"))
        self.assertTrue(is_campus_email("Juan@G.MSUIIT.EDU.PH"))
        self.assertFalse(is_campus_email("juan@gmail.com"))
        self.assertFalse(is_campus_email("juan@msuiit.edu.ph.evil.com"))
        self.assertFalse(is_campus_email(""))

    def test_non_campus_google_account_is_rejected(self):
        adapter = SocialAccountAdapter()
        sociallogin = SimpleNamespace(user=User(email="juan@gmail.com"), email_addresses=[])
        request = RequestFactory().get("/")
        with self.assertRaises(ImmediateHttpResponse) as ctx:
            adapter.pre_social_login(request, sociallogin)
        self.assertIn("error=domain", ctx.exception.response["Location"])

    def test_campus_google_account_is_allowed(self):
        adapter = SocialAccountAdapter()
        sociallogin = SimpleNamespace(user=User(email="juan@g.msuiit.edu.ph"), email_addresses=[])
        request = RequestFactory().get("/")
        adapter.pre_social_login(request, sociallogin)  # no exception
        self.assertTrue(adapter.is_open_for_signup(request, sociallogin))


class SignInPageTests(TestCase):
    def test_login_page_has_google_button(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertContains(response, "Sign in with MSU-IIT Google account")

    def test_login_page_shows_domain_error(self):
        response = self.client.get(reverse("accounts:login") + "?error=domain")
        self.assertContains(response, "Use your MSU-IIT email")

    def test_signed_out_user_is_sent_to_login(self):
        response = self.client.get(reverse("listings:home"))
        self.assertRedirects(response, reverse("accounts:login") + "?next=/", fetch_redirect_response=False)


class RoleRedirectTests(TestCase):
    def test_member_lands_on_browse(self):
        self.client.force_login(make_user("member"))
        response = self.client.get(reverse("accounts:after_login"))
        self.assertRedirects(response, reverse("listings:home"))

    def test_sid_staff_lands_on_dashboard(self):
        self.client.force_login(make_user("staff", role=User.Role.SID))
        response = self.client.get(reverse("accounts:after_login"))
        self.assertRedirects(response, reverse("accounts:sid_dashboard"))

    def test_member_cannot_open_sid_pages(self):
        self.client.force_login(make_user("member"))
        response = self.client.get(reverse("accounts:sid_dashboard"))
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "This page is for SID staff only", status_code=403)

    def test_email_is_unique(self):
        make_user("a")
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="b", email="a@g.msuiit.edu.ph", password="x")
