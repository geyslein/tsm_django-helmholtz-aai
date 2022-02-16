from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth import login as auth_login

from django_helmholtz_aai import signals

from . import _version

if TYPE_CHECKING:
    from django_helmholtz_aai import models

__version__ = _version.get_versions()["version"]


def login(request, user: models.HelmholtzUser, userinfo: dict[str, Any]):
    """Login the django user."""
    auth_login(request, user)

    # emit the aai_user_logged_in signal as an existing user has been
    # logged in
    signals.aai_user_logged_in.send(
        sender=user.__class__,
        user=user,
        request=request,
        userinfo=userinfo,
    )
