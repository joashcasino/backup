"""Sign-in rules for MyFinder (US-16).

- Only Google accounts on settings.ALLOWED_EMAIL_DOMAIN may sign in.
- Nobody can sign up with a password. Accounts are created on the first
  Google sign-in, or by an admin (for SID staff).
- After sign-in, users land on the page for their role.
"""
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from allauth.account.adapter import DefaultAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


def is_campus_email(email):
    email = (email or "").strip().lower()
    return email.endswith("@" + settings.ALLOWED_EMAIL_DOMAIN.lower())


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # No password sign-ups. Google sign-in has its own rule below.
        return False

    def get_login_redirect_url(self, request):
        return reverse("accounts:after_login")


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email or next(
            (e.email for e in sociallogin.email_addresses), ""
        )
        if not is_campus_email(email):
            # Error state D01b / M01b
            raise ImmediateHttpResponse(redirect(reverse("accounts:login") + "?error=domain"))

    def is_open_for_signup(self, request, sociallogin):
        return is_campus_email(sociallogin.user.email)

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if not user.username:
            user.username = (user.email or "").split("@")[0][:150]
        return user

    def on_authentication_error(self, request, provider, error=None, exception=None, extra_context=None):
        # Cancelled or failed Google sign-in: back to the sign-in page with a message.
        raise ImmediateHttpResponse(redirect(reverse("accounts:login") + "?error=failed"))
