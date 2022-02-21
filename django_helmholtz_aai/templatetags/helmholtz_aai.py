"""Template tags for the Helmholtz AAI."""


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


from urllib.parse import parse_qs, urlparse, urlunparse

from django import template
from django.urls import reverse
from django.utils.http import urlencode

register = template.Library()


@register.simple_tag(takes_context=True)
def helmholtz_login_url(context) -> str:
    """Get the url to login to the Helmholtz AAI."""
    login_url = reverse("django_helmholtz_aai:login")

    request = context["request"]

    parts = urlparse(request.path)
    urlparams = parse_qs(request.GET.urlencode())
    url = urlunparse(
        [
            parts.scheme,
            parts.netloc,
            login_url,
            parts.params,
            urlencode(urlparams, doseq=True),
            parts.fragment,
        ]
    )

    return url
