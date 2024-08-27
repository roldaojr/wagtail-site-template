import tempfile

from .settings import *  # NOQA
from .settings import STORAGES

MEDIA_ROOT = tempfile.gettempdir()
STORAGES["default"]["BACKEND"] = "django.core.files.storage.FileSystemStorage"
