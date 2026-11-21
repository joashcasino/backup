from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .decorators import sid_required

LOGIN_ERRORS = {
    "domain": "Use your MSU-IIT email (@g.msuiit.edu.ph) to sign in.",
    "failed": "Sign-in was cancelled or did not finish. Please try again.",
}


def login_view(request):
    """D01 / M01: one button, Sign in with MSU-IIT Google account."""
    if request.user.is_authenticated:
        return redirect("accounts:after_login")
    error = LOGIN_ERRORS.get(request.GET.get("error", ""))
    return render(request, "accounts/login.html", {"error": error})


@login_required
def after_login(request):
    """Send each user to the home page for their role."""
    if request.user.is_sid:
        return redirect("accounts:sid_dashboard")
    return redirect("listings:home")


@sid_required
def sid_dashboard(request):
    """S01 placeholder. Replace with the item register (US-09, US-11, US-17)."""
    return render(request, "accounts/sid_dashboard.html")
