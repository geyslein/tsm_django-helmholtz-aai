"""Admin interfaces
----------------

This module defines the django Helmholtz AAI Admin interfaces, based upon the
interfaces from :mod:`django.contrib.auth.admin`.
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


from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from django_helmholtz_aai import models


@admin.register(models.HelmholtzUser)
class HelmholtzAAIUserAdmin(UserAdmin):

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "eduperson_unique_id",
        "is_staff",
    )


@admin.register(models.HelmholtzVirtualOrganization)
class HelmholtzVirtualOrganizationAdmin(GroupAdmin):

    list_display = ("name", "eduperson_entitlement")
