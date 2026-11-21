from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def sid_required(view_func):
    """Allow only SID staff. Everyone else sees the access denied page (S10)."""

    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_sid:
            return render(request, "accounts/access_denied.html", status=403)
        return view_func(request, *args, **kwargs)

    return wrapper


class SIDRequiredMixin:
    """Class-based view version of @sid_required."""

    def dispatch(self, request, *args, **kwargs):
        return sid_required(super().dispatch)(request, *args, **kwargs)
