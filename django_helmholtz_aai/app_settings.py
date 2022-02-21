"""App settings
------------

This module defines the settings options for the ``django_helmholtz_aai`` app.
"""


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


from __future__ import annotations

import re
import warnings

from django.conf import settings

#: A string of lists that specify which VOs are allowed to log into the
#: website.
#:
#: By default, this is an empty list meaning that each and every user
#: is allowed to login via the Helmholtz AAI. Each string in this list will be
#: interpreted as a regular expression and added to :attr:`HELMHOLTZ_ALLOWED_VOS_REGEXP`
HELMHOLTZ_ALLOWED_VOS: list[str] = getattr(
    settings, "HELMHOLTZ_ALLOWED_VOS", []
)

#: Regular expressions for VOs that are allowed to login to the website.
#:
#: This attribute is created from the :attr:`HELMHOLTZ_ALLOWED_VOS` setting.
HELMHOLTZ_ALLOWED_VOS_REGEXP: list[re.Pattern] = getattr(
    settings, "HELMHOLTZ_ALLOWED_VOS_REGEXP", []
)

HELMHOLTZ_ALLOWED_VOS_REGEXP.extend(
    map(re.compile, HELMHOLTZ_ALLOWED_VOS)  # type: ignore
)

#: openid configuration url of the Helmholtz AAI
#:
#: Can also be overwritten using the :attr:`HELMHOLTZ_CLIENT_KWS` setting.
HELMHOLTZ_AAI_CONF_URL = (
    "https://login.helmholtz.de/oauth2/.well-known/openid-configuration"
)


#: Client id for the Helmholtz AAI
#:
#: This is the username you use to login at
#: https://login.helmholtz.de/oauthhome/, see
#: https://hifis.net/doc/helmholtz-aai/howto-services/ for how to create a
#: client
#:
#: See Also
#: --------
#: HELMHOLTZ_CLIENT_SECRET
HELMHOLTZ_CLIENT_ID: str = getattr(settings, "HELMHOLTZ_CLIENT_ID", "")


#: Client secret for the Helmholtz AAI
#:
#: This is the password you use to login at
#: https://login.helmholtz.de/oauthhome/, see
#: https://hifis.net/doc/helmholtz-aai/howto-services/ for how to create a
#: client.
#:
#: See Also
#: --------
#: HELMHOLTZ_CLIENT_ID
HELMHOLTZ_CLIENT_SECRET: str = getattr(settings, "HELMHOLTZ_CLIENT_SECRET", "")


if not HELMHOLTZ_CLIENT_ID:
    warnings.warn(
        "No client ID configured for the Helmholtz AAI. The authentification "
        "agains the Helmholtz AAI will not work! Please register a client and "
        "specify set the username as HELMHOLTZ_CLIENT_ID in settings.py.\n"
        "See https://hifis.net/doc/helmholtz-aai/howto-services/ for more "
        "information."
    )


if not HELMHOLTZ_CLIENT_SECRET:
    warnings.warn(
        "No client secret configured for the Helmholtz AAI. The "
        "authentification against the Helmholtz AAI will not work! Please "
        "register a client and set the secret as HELMHOLTZ_CLIENT_SECRET in "
        "settings.py.\n"
        "See https://hifis.net/doc/helmholtz-aai/howto-services/ for more "
        "information."
    )


#: Keyword argument for the oauth client to connect with the helmholtz AAI.
#:
#: Can also be overwritten using the :attr:`HELMHOLTZ_CLIENT_KWS` setting.
HELMHOLTZ_CLIENT_KWS = dict(
    client_id=HELMHOLTZ_CLIENT_ID,
    client_secret=HELMHOLTZ_CLIENT_SECRET,
    server_metadata_url=HELMHOLTZ_AAI_CONF_URL,
    client_kwargs={"scope": "profile email eduperson_unique_id"},
)

for key, val in getattr(settings, "HELMHOLTZ_CLIENT_KWS", {}).items():
    HELMHOLTZ_CLIENT_KWS[key] = val

#: Allow duplicated emails for users in the website
#:
#: This setting controls if a user can register with multiple accounts from the
#: Helmholtz AAI. An email is not unique in the AAI, but this might be desired
#: in the Django application. This option prevents a user to create an account
#: if the email has already been taken by some other user from the Helmholtz
#: AAI
HELMHOLTZ_EMAIL_DUPLICATES_ALLOWED: bool = getattr(
    settings, "HELMHOLTZ_EMAIL_DUPLICATES_ALLOWED", False
)
