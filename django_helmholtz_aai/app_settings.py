# Disclaimer
# ----------
#
# Copyright (C) 2022 Helmholtz-Zentrum Hereon
#
# This file is part of django-helmholtz-aai and is released under the
# EUPL-1.2 license.
# See LICENSE in the root of the repository for full licensing details.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the EUROPEAN UNION PUBLIC LICENCE v. 1.2 or later
# as published by the European Commission.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# EUPL-1.2 license for more details.
#
# You should have received a copy of the EUPL-1.2 license along with this
# program. If not, see https://www.eupl.eu/.


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

HELMHOLTZ_EMAIL_DUPLICATES_ALLOWED: bool = getattr(
    settings, "HELMHOLTZ_EMAIL_DUPLICATES_ALLOWED", False
)
