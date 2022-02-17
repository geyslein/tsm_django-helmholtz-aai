from __future__ import annotations

import re
from itertools import product
from typing import Any, Dict

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views import generic

from django_helmholtz_aai import app_settings
from django_helmholtz_aai import login as aai_login
from django_helmholtz_aai import models, signals

oauth = OAuth()

SCOPES = [
    "profile",
    "email",
    "eduperson_unique_id",
]


oauth.register(name="helmholtz", **app_settings.HELMHOLTZ_CLIENT_KWS)


User = get_user_model()

group_patt = re.compile(r".*:group:.*#.*")


class HelmholtzLoginView(LoginView):
    """A login view for the Helmholtz AAI that forwards to the OAuth login."""

    def get(self, request):
        redirect_uri = request.build_absolute_uri(
            reverse("django_helmholtz_aai:auth")
        )
        request.session["forward_after_aai_login"] = self.get_success_url()
        return oauth.helmholtz.authorize_redirect(request, redirect_uri)

    def post(self, request):
        return self.get(request)


class HelmholtzAuthentificationView(PermissionRequiredMixin, generic.View):
    """Authentification view for the Helmholtz AAI."""

    raise_exception = True

    @cached_property
    def userinfo(self) -> Dict[str, Any]:
        token = oauth.helmholtz.authorize_access_token(self.request)
        return oauth.helmholtz.userinfo(request=self.request, token=token)

    def login_user(self, user: models.HelmholtzUser):
        """Login the django user."""
        aai_login(self.request, user, self.userinfo)

    def get(self, request):

        user = self.get_or_create_user()
        self.synchronize_vos(user, self.userinfo["eduperson_entitlement"])

        self.login_user(user)

        return_url = request.session.pop(
            "forward_after_aai_login", settings.LOGIN_REDIRECT_URL
        )

        return redirect(return_url)

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

    @staticmethod
    def _username_exists(username: str):
        return bool(models.HelmholtzUser.objects.filter(username=username))

    @staticmethod
    def _email_exists(email: str) -> bool:
        return bool(models.HelmholtzUser.objects.filter(email=email))

    def create_user(self, userinfo: Dict[str, Any]) -> models.HelmholtzUser:
        """Create a Django user for a Helmholtz AAI User."""

        username = userinfo["preferred_username"]
        email = userinfo["email"]

        if self._username_exists(username):
            username = userinfo["email"]
        if self._email_exists(email):
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

        # emit the aai_user_created signal after the user has been created
        signals.aai_user_created.send(
            sender=user.__class__,
            user=user,
            request=self.request,
            userinfo=userinfo,
        )
        return user

    def update_user(
        self, user: models.HelmholtzUser, userinfo: Dict[str, Any]
    ):
        """Update the user from the provided information."""
        to_update = {}

        username = userinfo["preferred_username"]
        email = userinfo["email"]

        if user.username != username and not self._username_exists(username):
            if not User.objects.filter(username=username):
                to_update["username"] = username
        if user.first_name != userinfo["given_name"]:
            to_update["first_name"] = userinfo["given_name"]
        if user.last_name != userinfo["family_name"]:
            to_update["last_name"] = userinfo["family_name"]
        if user.email != email:
            if self._email_exists(email):
                self.permission_denied_message = (
                    f"A user with the email {email} already exists."
                )
                self.handle_no_permission()
            to_update["email"] = email
        if to_update:
            for key, val in to_update.items():
                setattr(user, key, val)
            user.save()

            # emit the aai_user_updated signal as the user has been updated
            signals.aai_user_updated.send(
                sender=user.__class__,
                user=user,
                request=self.request,
                userinfo=userinfo,
            )

    def get_or_create_user(self) -> models.HelmholtzUser:

        userinfo = self.userinfo

        if not userinfo.get("preferred_username"):
            userinfo["preferred_username"] = userinfo["email"]
        try:
            user = models.HelmholtzUser.objects.get(
                eduperson_unique_id=userinfo["eduperson_unique_id"]
            )
        except models.HelmholtzUser.DoesNotExist:
            user = self.create_user(userinfo)
        else:
            self.update_user(user, userinfo)

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
            signals.aai_vo_left.send(
                sender=vo.__class__,
                request=self.request,
                user=user,
                vo=vo,
                userinfo=self.userinfo,
            )

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
                signals.aai_vo_created.send(
                    sender=vo.__class__,
                    request=self.request,
                    vo=vo,
                    userinfo=self.userinfo,
                )
            user.groups.add(vo)
            signals.aai_vo_entered.send(
                sender=vo.__class__,
                request=self.request,
                user=user,
                vo=vo,
                userinfo=self.userinfo,
            )
