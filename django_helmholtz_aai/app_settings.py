import re

from django.conf import settings

HELMHOLTZ_ALLOWED_VOS = list(
    map(re.compile, getattr(settings, "HELMHOLTZ_ALLOWED_VOS", []))
)
