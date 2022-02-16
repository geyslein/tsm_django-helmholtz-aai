from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models


class HelmholtzUser(get_user_model()):  # type: ignore
    """A User in the in the Helmholtz AAI."""

    eduperson_unique_id = models.CharField(max_length=500, unique=True)


class HelmholtzVirtualOrganization(Group):
    """A VO in the Helmholtz AAI."""

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
