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
