from django.conf import settings
from django.core.files.storage import FileSystemStorage


class PrivateStorage(FileSystemStorage):
    """Storage for files that must never get a public URL.

    Files live outside MEDIA_ROOT, and .url() is disabled so a template cannot
    link to them by mistake. Serve them through a view that checks permissions,
    such as claims.views.proof_photo.
    """

    def url(self, name):
        raise ValueError(
            "Private files have no public URL. Link to the permission-checked view instead "
            "(e.g. {% url 'claims:proof_photo' claim.pk %})."
        )


private_storage = PrivateStorage(location=settings.PRIVATE_MEDIA_ROOT)


def get_private_storage():
    # Used as a callable in the model, so migrations don't record a machine-specific path.
    return private_storage
