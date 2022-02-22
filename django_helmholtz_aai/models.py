"""Models
======

Models to mimic users and virtual organizations of the Helmholtz AAI in Django.
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
from typing import TYPE_CHECKING, Callable

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, GroupManager
from django.db import models

from django_helmholtz_aai import app_settings

if TYPE_CHECKING:
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class HelmholtzUserManager(User.objects.__class__):  # type: ignore
    """A manager for the helmholtz User."""

    def create_aai_user(self, userinfo):
        """Create a user from the Helmholtz AAI userinfo."""

        for field in app_settings.HELMHOLTZ_USERNAME_FIELDS:
            username = userinfo.get(field)
            if username and not self.filter(username=username):
                break

        email = userinfo["email"]

        user = self.create(
            username=username,
            first_name=userinfo["given_name"],
            last_name=userinfo["family_name"],
            email=email,
            eduperson_unique_id=userinfo["eduperson_unique_id"],
        )
        return user


class HelmholtzUser(User):
    """A User in the in the Helmholtz AAI."""

    objects = HelmholtzUserManager()

    eduperson_unique_id = models.CharField(max_length=500, unique=True)


class HelmholtzVirtualOrganizationQuerySet(models.QuerySet):
    """A queryset with an extra command to remove empty VOs."""

    def remove_empty_vos(
        self,
        exclude: list[str] = [],
        without_confirmation: bool = True,
    ) -> list[HelmholtzVirtualOrganization]:
        """Remove empty virtual organizations.

        This method filters for virtual organizations in the queryset and
        removes them.

        Parameters
        ----------
        exclude: list[str]
            A list of strings that will be interpreted as regular expressions.
            If a :attr:`~HelmholtzVirtualOrganization.eduperson_entitlement`
            matches any of these strings, it will not be removed.
        without_confirmation: bool
            If True (default), remove the VO without asking for confirmation
            using python's built-in :func:`input` from the command-line.

        Returns
        -------
        list[HelmholtzVirtualOrganization]
            The list of virtual organizations that have been removed
        """
        exclude_regex: Callable[str] = list(map(re.compile, exclude))  # type: ignore
        vo: HelmholtzVirtualOrganization
        removed: list[HelmholtzVirtualOrganization] = []
        for vo in self.annotate(count=models.Count("user")).filter(count=0):
            if not any(
                patt.match(vo.eduperson_entitlement) for patt in exclude_regex
            ):
                if without_confirmation:
                    vo.delete()
                    removed.append(vo)
                else:
                    answer = ""
                    while answer not in ["y", "n"]:
                        answer = input(f"Remove {vo}? [y/n]").lower()
                    if answer == "y":
                        vo.delete()
                        removed.append(vo)
        return removed


class HelmholtzVirtualOrganizationManager(
    GroupManager.from_queryset(HelmholtzVirtualOrganizationQuerySet)  # type: ignore
):
    """Database manager for the :class:`HelmholtzVirtualOrganization` model."""


class HelmholtzVirtualOrganization(Group):
    """A VO in the Helmholtz AAI."""

    objects = HelmholtzVirtualOrganizationManager()

    eduperson_entitlement = models.CharField(max_length=500, unique=True)

    @property
    def display_name(self) -> str:
        return self.name.split(":group:", maxsplit=1)[1]

    def __str__(self) -> str:
        return self.display_name


def _display_group_name(self):
    if hasattr(self, "helmholtzvirtualorganization"):
        return self.helmholtzvirtualorganization.display_name
    return self.name


Group.add_to_class("__str__", _display_group_name)
