from __future__ import annotations

import re
from itertools import product
from typing import Any, Dict

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.contrib import messages
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

    _permission_denied: bool = False

    aai_user: models.HelmholtzUser

    @cached_property
    def userinfo(self) -> Dict[str, Any]:
        token = oauth.helmholtz.authorize_access_token(self.request)
        return oauth.helmholtz.userinfo(request=self.request, token=token)

    def login_user(self, user: models.HelmholtzUser):
        """Login the django user."""
        aai_login(self.request, user, self.userinfo)

    def get(self, request):

        if self.is_new_user:
            self.aai_user = self.create_user(self.userinfo)
        else:
            self.update_user()

        self.synchronize_vos()

        self.login_user(self.aai_user)

        return_url = request.session.pop(
            "forward_after_aai_login", settings.LOGIN_REDIRECT_URL
        )

        return redirect(return_url)

    def handle_no_permission(self):
        messages.add_message(
            self.request, messages.ERROR, self.permission_denied_message
        )
        return super().handle_no_permission()

    @cached_property
    def is_new_user(self) -> bool:
        try:
            self.aai_user = models.HelmholtzUser.objects.get(
                eduperson_unique_id=self.userinfo["eduperson_unique_id"]
            )
        except models.HelmholtzUser.DoesNotExist:
            return True
        else:
            return False

    def has_permission(self) -> bool:

        userinfo = self.userinfo
        email = userinfo["email"]

        # check if the user belongs to the allowed VOs
        if app_settings.HELMHOLTZ_ALLOWED_VOS:
            if not any(
                patt.match(vo)
                for patt, vo in product(
                    app_settings.HELMHOLTZ_ALLOWED_VOS,
                    userinfo["eduperson_entitlement"],
                )
            ):
                self.permission_denied_message = (
                    "Your virtual organizations are not allowed to log into "
                    "this website."
                )
                return False

        # check for email verification
        if not userinfo["email_verified"]:
            self.permission_denied_message = (
                "Your email has not been verified."
            )
            return False

        # check for email duplicates
        if not self.is_new_user:
            # check if we need to update the email and if yes, check if this
            # is possible
            if self.aai_user.email != email:
                if self._email_exists(email):
                    self.permission_denied_message = (
                        f"A user with the email {email} already exists."
                    )
                    return False
        elif self._email_exists(email):
            self.permission_denied_message = (
                f"A user with the email {email} already exists."
            )
            return False

        return True

    @staticmethod
    def _username_exists(username: str):
        return bool(models.HelmholtzUser.objects.filter(username=username))

    @staticmethod
    def _email_exists(email: str) -> bool:
        if app_settings.HELMHOLTZ_EMAIL_DUPLICATES_ALLOWED:
            return False
        return bool(models.HelmholtzUser.objects.filter(email=email))

    def create_user(self, userinfo: Dict[str, Any]) -> models.HelmholtzUser:
        """Create a Django user for a Helmholtz AAI User."""

        user = models.HelmholtzUser.objects.create_aai_user(self.userinfo)

        # emit the aai_user_created signal after the user has been created
        signals.aai_user_created.send(
            sender=user.__class__,
            user=user,
            request=self.request,
            userinfo=userinfo,
        )
        return user

    def update_user(self):
        """Update the user from the provided information."""
        to_update = {}

        userinfo = self.userinfo
        user = self.aai_user

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

    def synchronize_vos(self):

        user = self.aai_user
        vos = self.userinfo["eduperson_entitlement"]

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
            except models.HelmholtzVirtualOrganization.DoesNotExist:  # pylint: disable=no-member
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
