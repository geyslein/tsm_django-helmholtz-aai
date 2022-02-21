from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models

if TYPE_CHECKING:
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class HelmholtzUserManager(User.objects.__class__):  # type: ignore
    """A manager for the helmholtz User."""

    def create_aai_user(self, userinfo):
        """Create a user from the Helmholtz AAI userinfo."""

        username = userinfo["preferred_username"]
        email = userinfo["email"]

        if self._username_exists(username):
            username = userinfo["eduperson_unique_id"]
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
