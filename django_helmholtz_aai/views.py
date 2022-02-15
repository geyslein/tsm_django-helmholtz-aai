from __future__ import annotations

import re
from itertools import product
from typing import Any, Dict

from authlib.integrations.django_client import OAuth
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views import generic

from django_helmholtz_aai import app_settings, models

CONF_URL = "https://login.helmholtz.de/oauth2/.well-known/openid-configuration"
oauth = OAuth()

SCOPES = [
    "credentials",
    "openid",
    "profile",
    "display_name",
    "eduperson_entitlement",
    "eduperson_principal_name",
    "offline_access",
    "eduperson_scoped_affiliation",
    "eduperson_unique_id",
    "sn",
    "eduperson_assurance",
    "email",
    "single-logout",
]


oauth.register(
    name="helmholtz",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": " ".join(SCOPES)},
)


User = get_user_model()

group_patt = re.compile(r".*:group:.*#.*")


def login(request):
    redirect_uri = request.build_absolute_uri(
        reverse("django_helmholtz_aai:auth")
    )
    return oauth.helmholtz.authorize_redirect(request, redirect_uri)


class HelmholtzAuthentificationView(PermissionRequiredMixin, generic.View):
    """Authentification view for the Helmholtz AAI."""

    raise_exception = True

    @cached_property
    def userinfo(self) -> Dict[str, Any]:
        token = oauth.helmholtz.authorize_access_token(self.request)
        return oauth.helmholtz.userinfo(request=self.request, token=token)

    def get(self, request):

        user = self.get_or_create_user()
        self.synchronize_vos(user, self.userinfo["eduperson_entitlement"])

        auth_login(request, user)

        return redirect(reverse("home"))

    def has_permission(self) -> bool:

        if app_settings.HELMHOLTZ_ALLOWED_VOS:
            if not any(
                patt.match(vo)
                for patt, vo in product(
                    app_settings.HELMHOLTZ_ALLOWED_VOS,
                    self.userinfo["eduperson_entitlement"],
                )
            ):
                self.permission_denied_message = (
                    "Your virtual organization is not allowed to log into "
                    "this website."
                )
                return False
        if not self.userinfo["email_verified"]:
            self.permission_denied_message = (
                "Your email has not been verified."
            )
            return False
        return True

    def get_or_create_user(self) -> models.HelmholtzUser:
        def username_exists() -> bool:
            return bool(models.HelmholtzUser.objects.filter(username=username))

        def email_exists() -> bool:
            return bool(models.HelmholtzUser.objects.filter(email=email))

        userinfo = self.userinfo

        # try if we find a user
        username = userinfo["preferred_username"]
        email = userinfo["email"]
        if not username:
            username = userinfo["email"]
        try:
            user = models.HelmholtzUser.objects.get(
                eduperson_unique_id=userinfo["eduperson_unique_id"]
            )
        except models.HelmholtzUser.DoesNotExist:
            # test for user name
            # if the preferred_username already exists, we use the mail address
            if username_exists():
                username = userinfo["email"]
            if email_exists():
                self.permission_denied_message = (
                    f"A user with the email {email} already exists."
                )
                self.handle_no_permission()
            user = models.HelmholtzUser.objects.create(
                username=username,
                first_name=userinfo["given_name"],
                last_name=userinfo["family_name"],
                email=email,
                eduperson_unique_id=userinfo["eduperson_unique_id"],
            )
        else:
            to_update = {}
            if user.username != username and not username_exists():
                if not User.objects.filter(username=username):
                    to_update["username"] = username
            if user.first_name != userinfo["given_name"]:
                to_update["first_name"] = userinfo["given_name"]
            if user.last_name != userinfo["family_name"]:
                to_update["last_name"] = userinfo["family_name"]
            if user.email != userinfo["email"]:
                if email_exists():
                    self.permission_denied_message = (
                        f"A user with the email {email} already exists."
                    )
                    self.handle_no_permission()
                to_update["email"] = email
            if to_update:
                for key, val in to_update.items():
                    setattr(user, key, val)
                user.save()
        return user

    def synchronize_vos(self, user, vos):

        # synchronize VOs
        current_vos = user.groups.filter(
            helmholtzvirtualorganization__isnull=False
        )
        if current_vos:
            vo_names = [
                t[0]
                for t in current_vos.values_list(
                    "helmholtzvirtualorganization__eduperson_entitlement"
                )
            ]
        else:
            vo_names = []
        actual_vos = list(filter(group_patt.match, vos))

        # remove VOs in the database
        for vo_name in set(vo_names) - set(actual_vos):
            vo = models.HelmholtzVirtualOrganization.objects.get(
                eduperson_entitlement=vo_name
            )
            user.groups.remove(vo)

        # add new VOs in the database
        for vo_name in set(actual_vos) - set(vo_names):
            try:
                vo = models.HelmholtzVirtualOrganization.objects.get(
                    eduperson_entitlement=vo_name
                )
            except models.HelmholtzVirtualOrganization.DoesNotExist:
                vo = models.HelmholtzVirtualOrganization.objects.create(
                    name=vo_name, eduperson_entitlement=vo_name
                )
            user.groups.add(vo)
