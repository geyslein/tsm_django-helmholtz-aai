"""Django Helmholtz AAI

Generic Django app for connecting with the Helmholtz AAI.
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

from typing import TYPE_CHECKING, Any

from django.contrib.auth import login as auth_login

from django_helmholtz_aai import signals

from . import _version

if TYPE_CHECKING:
    from django_helmholtz_aai import models

__version__ = _version.get_versions()["version"]

__author__ = "Phiilpp S. Sommer, Housam Dibeh, Hatef Takyar"
__copyright__ = "Copyright (C) 2022 Helmholtz-Zentrum Hereon"
__credits__ = ["Philipp S. Sommer", "Housam Dibeh", "Hatef Takyar"]
__license__ = "EUPL-1.2"

__maintainer__ = "Helmholtz Coastal Data Center"
__email__ = "hcdc_support@hereon.de"

__status__ = "Production"


def login(request, user: models.HelmholtzUser, userinfo: dict[str, Any]):
    """Login the helmholtz user into django.

    Notes
    -----
    Emits the :attr:`~django_helmholtz_aai.signals.aai_user_logged_in` signal
    """
    auth_login(request, user)

    # emit the aai_user_logged_in signal as an existing user has been
    # logged in
    signals.aai_user_logged_in.send(
        sender=user.__class__,
        user=user,
        request=request,
        userinfo=userinfo,
    )
