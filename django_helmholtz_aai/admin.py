from django.contrib import admin

from django_helmholtz_aai import models


@admin.register(models.HelmholtzUser)
class HelmholtzAAIUserAdmin(admin.ModelAdmin):

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "eduperson_unique_id",
    )


@admin.register(models.HelmholtzVirtualOrganization)
class HelmholtzVirtualOrganizationAdmin(admin.ModelAdmin):

    list_display = ("name", "eduperson_entitlement")
