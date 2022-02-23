"""Test for the Helmholtz Authentification View
-----------------------------------------------

This module defines unittests for the
:class:`django_helmholtz_aai.views.HelmholtzAuthentificationView` class.
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
from typing import TYPE_CHECKING, Any, Callable

import pytest
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.exceptions import PermissionDenied
from django.utils.functional import cached_property

from django_helmholtz_aai import app_settings, models, signals
from django_helmholtz_aai.views import HelmholtzAuthentificationView

if TYPE_CHECKING:
    from django.contrib.auth.models import User
    from django.test import RequestFactory


# -----------------------------------------------------------------------------
# ---------------------- fixtures ---------------------------------------------
# -----------------------------------------------------------------------------


@pytest.fixture
def userinfo() -> dict[str, Any]:
    return {
        "sub": "bdeba218-2342-3456-sad3-ff4sdfew2444",
        "email_verified": True,
        "name": "Firstname Lastname",
        "eduperson_unique_id": "bdeba21823423456sad3ff4sdfew2444@login.helmholtz-data-federation.de",
        "preferred_username": "dummy_user",
        "given_name": "Firstname",
        "family_name": "Lastname",
        "email": "user@example.com",
        "eduperson_entitlement": [
            "urn:geant:helmholtz.de:group:some_VO#login.helmholtz.de",
            "urn:geant:helmholtz.de:group:some_VO:subgroup#login.helmholtz.de",
            "urn:mace:dir:entitlement:common-lib-terms",
        ],
    }


@pytest.fixture
def username(userinfo: dict[str, Any]) -> str:
    return userinfo["preferred_username"]


class PatchedHelmholtzAuthentificationView(HelmholtzAuthentificationView):
    """Patched authentification view as we cannot test against the real AAI."""

    _userinfo: dict[str, Any]

    raise_exception = True

    @cached_property
    def userinfo(self) -> dict[str, Any]:
        return self._userinfo


@pytest.fixture
def authentification_view(db, rf: RequestFactory, userinfo: dict[str, Any]):

    request = rf.get("/helmholtz-aai/auth/")

    session_middleware = SessionMiddleware()
    session_middleware.process_request(request)
    request.session.save()

    auth_middleware = AuthenticationMiddleware()
    auth_middleware.process_request(request)

    message_middleware = MessageMiddleware()
    message_middleware.process_request(request)

    view = PatchedHelmholtzAuthentificationView()
    view._userinfo = userinfo
    view.setup(request)
    return view


@pytest.fixture
def patched_signals(monkeypatch) -> list[str]:
    """Patched signals."""

    signals_raised = []

    def send_factory(signal: str) -> Callable:
        def send(*args, **kwargs):
            signals_raised.append(signal)

        return send

    for signal in [
        "aai_user_created",
        "aai_user_logged_in",
        "aai_user_updated",
        "aai_vo_created",
        "aai_vo_entered",
        "aai_vo_left",
    ]:
        monkeypatch.setattr(
            getattr(signals, signal), "send", send_factory(signal)
        )
    return signals_raised


# -----------------------------------------------------------------------------
# ------------------------- tests ---------------------------------------------
# -----------------------------------------------------------------------------


def test_basic_get(
    authentification_view: PatchedHelmholtzAuthentificationView, username: str
):
    """Test basic login."""
    authentification_view.dispatch(authentification_view.request)

    assert models.HelmholtzUser.objects.get(username=username)

    authentification_view.is_new_user = False


def test_signal_user_created(
    authentification_view: PatchedHelmholtzAuthentificationView,
    patched_signals: list[str],
):
    """Test if the signal aai_user_created and aai_user_logged_in are fired."""
    authentification_view.dispatch(authentification_view.request)

    assert patched_signals[0] == "aai_user_created"
    assert patched_signals[-1] == "aai_user_logged_in"


def test_signal_vo_created(
    authentification_view: PatchedHelmholtzAuthentificationView,
    patched_signals: list[str],
):
    """Test if the signal aai_vo_created is fired on user creation."""
    authentification_view.dispatch(authentification_view.request)

    # we have two VOs in the userinfo, so this signal should be triggered twice
    assert patched_signals[1:-1:2] == ["aai_vo_created", "aai_vo_created"]


def test_signal_vo_entered(
    authentification_view: PatchedHelmholtzAuthentificationView,
    patched_signals: list[str],
):
    """Test if the signal aai_vo_entered is fired on user creation."""
    authentification_view.dispatch(authentification_view.request)

    # we have two VOs in the userinfo, so this signal should be triggered twice
    assert patched_signals[2:-1:2] == ["aai_vo_entered", "aai_vo_entered"]


def test_change_username(
    authentification_view: PatchedHelmholtzAuthentificationView,
    username: str,
    userinfo: dict[str, Any],
    patched_signals: list[str],
    monkeypatch,
):
    """Test what happens if the username changes."""
    test_basic_get(authentification_view, username)

    userinfo["preferred_username"] = "max.mustermann"

    test_basic_get(authentification_view, "max.mustermann")

    assert patched_signals[-2:] == ["aai_user_updated", "aai_user_logged_in"]

    # now test if we can prevent changing the username
    monkeypatch.setattr(
        app_settings,
        "HELMHOLTZ_UPDATE_USERNAME",
        False,
    )

    userinfo["preferred_username"] = "newusername"

    test_basic_get(authentification_view, "max.mustermann")


def test_helmholtz_username_fields(
    authentification_view: PatchedHelmholtzAuthentificationView,
    userinfo: dict[str, Any],
    monkeypatch,
):
    """Test changing the username fields."""
    monkeypatch.setattr(
        app_settings,
        "HELMHOLTZ_USERNAME_FIELDS",
        ["email", "eduperson_unique_id"],
    )

    test_basic_get(authentification_view, userinfo["email"])


def test_change_email(
    authentification_view: PatchedHelmholtzAuthentificationView,
    username: str,
    userinfo: dict[str, Any],
    patched_signals: list[str],
):
    """Test what happens if the email changes."""
    test_basic_get(authentification_view, username)

    orig_mail = userinfo["email"]

    assert models.HelmholtzUser.objects.get(email=orig_mail)

    new_mail = "newmail@example.com"
    userinfo["email"] = new_mail

    test_basic_get(authentification_view, username)

    assert models.HelmholtzUser.objects.get(email=new_mail)
    assert not models.HelmholtzUser.objects.filter(email=orig_mail)

    assert patched_signals[-2:] == ["aai_user_updated", "aai_user_logged_in"]


def test_email_duplicate(
    authentification_view: PatchedHelmholtzAuthentificationView,
    username: str,
    userinfo: dict[str, Any],
):
    """Test what happens if the username changes."""
    test_basic_get(authentification_view, username)

    orig_id = userinfo["eduperson_unique_id"]

    assert models.HelmholtzUser.objects.get(eduperson_unique_id=orig_id)

    new_id = orig_id + "123"
    userinfo["eduperson_unique_id"] = new_id
    authentification_view.is_new_user = True

    with pytest.raises(PermissionDenied):
        test_basic_get(authentification_view, username)

    assert not models.HelmholtzUser.objects.filter(eduperson_unique_id=new_id)
    assert models.HelmholtzUser.objects.get(eduperson_unique_id=orig_id)


def test_change_vo(
    authentification_view: PatchedHelmholtzAuthentificationView,
    username: str,
    userinfo: dict[str, Any],
    patched_signals: list[str],
):
    """Test what happens if the username changes."""
    test_basic_get(authentification_view, username)

    userinfo["eduperson_entitlement"].pop(1)

    patched_signals.clear()

    test_basic_get(authentification_view, username)

    assert patched_signals == ["aai_vo_left", "aai_user_logged_in"]


def test_allowed_vos(
    authentification_view: PatchedHelmholtzAuthentificationView,
    username: str,
    userinfo: dict[str, Any],
    monkeypatch,
):
    """Test login with HELMHOLTZ_ALLOWED_VOS."""
    test_basic_get(authentification_view, username)

    HELMHOLTZ_ALLOWED_VOS_REGEXP = [re.compile(r".*not_available.*")]

    monkeypatch.setattr(
        app_settings,
        "HELMHOLTZ_ALLOWED_VOS_REGEXP",
        HELMHOLTZ_ALLOWED_VOS_REGEXP,
    )

    with pytest.raises(PermissionDenied):
        test_basic_get(authentification_view, username)

    HELMHOLTZ_ALLOWED_VOS_REGEXP.append(re.compile(r".*:group:some_VO#.*"))

    test_basic_get(authentification_view, username)


def test_helmholtz_map_accounts(
    authentification_view: PatchedHelmholtzAuthentificationView,
    username: str,
    userinfo: dict[str, Any],
    admin_user: User,
    monkeypatch,
):
    """Test login with HELMHOLTZ_MAP_ACCOUNTS."""

    admin_user.email = userinfo["email"]
    admin_user.save()

    monkeypatch.setattr(
        app_settings,
        "HELMHOLTZ_MAP_ACCOUNTS",
        True,
    )

    test_basic_get(authentification_view, username)

    new_user = models.HelmholtzUser.objects.get(username=username)
    assert new_user.pk == admin_user.pk


def test_helmholtz_create_users(
    authentification_view: PatchedHelmholtzAuthentificationView,
    username: str,
    userinfo: dict[str, Any],
    monkeypatch,
):
    """Test preventing the creation of new users."""

    monkeypatch.setattr(
        app_settings,
        "HELMHOLTZ_CREATE_USERS",
        False,
    )

    with pytest.raises(PermissionDenied):
        test_basic_get(authentification_view, username)
