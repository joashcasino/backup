from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from .models import Claim


@login_required
def proof_photo(request, pk):
    """Serve a claim's proof photo to the claimant or SID staff only."""
    claim = get_object_or_404(Claim, pk=pk)
    if not claim.can_view(request.user) or not claim.proof_photo:
        # 404 instead of 403, so other users cannot tell whether a photo exists
        raise Http404
    return FileResponse(claim.proof_photo.open("rb"))
