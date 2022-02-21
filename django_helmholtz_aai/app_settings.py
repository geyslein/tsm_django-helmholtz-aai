import re

from django.conf import settings

HELMHOLTZ_ALLOWED_VOS = list(
    map(re.compile, getattr(settings, "HELMHOLTZ_ALLOWED_VOS", []))
)

CONF_URL = "https://login.helmholtz.de/oauth2/.well-known/openid-configuration"

HELMHOLTZ_CLIENT_KWS = dict(
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "profile email eduperson_unique_id"},
)

for key, val in getattr(settings, "HELMHOLTZ_CLIENT_KWS", {}).items():
    HELMHOLTZ_CLIENT_KWS[key] = val

HELMHOLTZ_EMAIL_DUPLICATES_ALLOWED: bool = False
