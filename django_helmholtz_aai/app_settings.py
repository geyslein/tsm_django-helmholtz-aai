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

#: A string of lists specifying which VOs are allowed to log into the website.
#:
#: By default, this is an empty list meaning that each and every user
#: is allowed to login via the Helmholtz AAI. Each string in this list will be
#: interpreted as a regular expression and added to :attr:`HELMHOLTZ_ALLOWED_VOS_REGEXP`
#:
#: .. setting:: HELMHOLTZ_ALLOWED_VOS
#:
#: Examples
#: --------
#: Assume you only want to allow people from the Hereon VO to login to the
#: website. Then you can add the following to your ``settings.py``::
#:
#:     HELMHOLTZ_ALLOWED_VOS = [
#:         "urn:geant:helmholtz.de:group:hereon#login.helmholtz.de",
#:     ]
#:
#: or use a regex, e.g. something like::
#:
#:     HELMHOLTZ_ALLOWED_VOS = [
#:         r".*helmholtz.de:group:hereon#login.helmholtz.de",
#:     ]
HELMHOLTZ_ALLOWED_VOS: list[str] = getattr(
    settings, "HELMHOLTZ_ALLOWED_VOS", []
)

#: Regular expressions for VOs that are allowed to login to the website.
#:
#: This attribute is created from the :attr:`HELMHOLTZ_ALLOWED_VOS` setting.
#:
#: .. setting:: HELMHOLTZ_ALLOWED_VOS_REGEXP
HELMHOLTZ_ALLOWED_VOS_REGEXP: list[re.Pattern] = getattr(
    settings, "HELMHOLTZ_ALLOWED_VOS_REGEXP", []
)

HELMHOLTZ_ALLOWED_VOS_REGEXP.extend(
    map(re.compile, HELMHOLTZ_ALLOWED_VOS)  # type: ignore
)

#: openid configuration url of the Helmholtz AAI
#:
#: Can also be overwritten using the :attr:`HELMHOLTZ_CLIENT_KWS` setting.
#:
#: .. setting:: HELMHOLTZ_AAI_CONF_URL
HELMHOLTZ_AAI_CONF_URL = (
    "https://login.helmholtz.de/oauth2/.well-known/openid-configuration"
)


#: Client id for the Helmholtz AAI
#:
#: This is the username you use to login at
#: https://login.helmholtz.de/oauthhome/, see [client-registration]_ for how to
#: create a client
#:
#: .. setting:: HELMHOLTZ_CLIENT_ID
#:
#: See Also
#: --------
#: HELMHOLTZ_CLIENT_SECRET
HELMHOLTZ_CLIENT_ID: str = getattr(settings, "HELMHOLTZ_CLIENT_ID", "")


#: Client secret for the Helmholtz AAI
#:
#: This is the password you use to login at
#: https://login.helmholtz.de/oauthhome/, see[client-registration]_ for how to
#: create a client
#:
#: .. setting:: HELMHOLTZ_CLIENT_SECRET
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
#:
#: .. setting:: HELMHOLTZ_CLIENT_KWS
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
#:
#: .. setting:: HELMHOLTZ_EMAIL_DUPLICATES_ALLOWED
HELMHOLTZ_EMAIL_DUPLICATES_ALLOWED: bool = getattr(
    settings, "HELMHOLTZ_EMAIL_DUPLICATES_ALLOWED", False
)


#: Username fields in the userinfo
#:
#: This setting determines how to get the username. By default, we use the
#: ``preferred_username`` that the user can configure at
#: https://login.helmholtz.de/oauthhome. If this is already taken, we use the
#: unique ``eduperson_unique_id`` from the Helmholtz AAI. You can add more
#: variables to this list but you should always include the
#: ``eduperson_unique_id`` to make sure you do not end up with duplicated
#: usernames.
#:
#: .. setting:: HELMHOLTZ_USERNAME_FIELDS
#:
#: Examples
#: --------
#: You can use the email instead of the ``preferred_username`` via::
#:
#:     HELMHOLTZ_USERNAME_FIELDS = ["email", "eduperson_unique_id"]
HELMHOLTZ_USERNAME_FIELDS: list[str] = getattr(
    settings,
    "HELMHOLTZ_USERNAME_FIELDS",
    ["preferred_username", "eduperson_unique_id"],
)


#: Flag whether usernames should be updated from the Helmholtz AAI
#:
#: Use this setting to control, whether the usernames are updated automatically
#: on every login. If this is true, we will check the fields specified in the
#: :attr:`HELMHOLTZ_USERNAME_FIELDS` setting variable on every login and update
#: the username accordingly. If the user, for instance, changes his or her
#: ``preferred_username`` on https://login.helmholtz.de/, we will update the
#: username of the django user as well (if ``preferred_username`` is in the
#: :attr:`HELMHOLTZ_USERNAME_FIELDS`).
#:
#: .. setting:: HELMHOLTZ_UPDATE_USERNAME
HELMHOLTZ_UPDATE_USERNAME: bool = getattr(
    settings, "HELMHOLTZ_UPDATE_USERNAMES", True
)


#: Flag whether existing user accounts should be mapped
#:
#: Use this flag, if you want to map existing user accounts by their email
#: address.
#:
#: ..setting:: HELMHOLTZ_MAP_ACCOUNTS
#:
#: Examples
#: --------
#: Suppose you just install django-helmholtz-aai to your already existing
#: Django project and there exists already a user with the mail
#: ``user@example.com``. If this user now logs into your project, it would
#: create a new :class:`~django_helmholtz_aai.models.HelmholtzUser` which is
#: probably not desired. To overcome this, you can set the
#: :setting:`HELMHOLTZ_MAP_ACCOUNTS` configuration variable to ``True`` and the
#: :class:`~django_helmholtz_aai.models.HelmholtzUser` will be mapped to the
#: already existing :class:`~django.contrib.auth.models.User`
HELMHOLTZ_MAP_ACCOUNTS: bool = getattr(
    settings, "HELMHOLTZ_MAP_ACCOUNTS", False
)

#: Flag to enable/disable user account creation via the Helmholtz AAI.
#:
#: Use this flag if you want the Helmholtz AAI to create users when they login
#: for the first time. This is enabled by default.
#:
#: If you disable this setting, you should enable the
#: :setting:`HELMHOLTZ_MAP_ACCOUNTS`, otherwise nobody will be allowed to
#: login via the Helmholtz AAI.
#:
#: .. setting:: HELMHOLTZ_CREATE_USERS
HELMHOLTZ_CREATE_USERS: bool = getattr(
    settings, "HELMHOLTZ_CREATE_USERS", True
)
