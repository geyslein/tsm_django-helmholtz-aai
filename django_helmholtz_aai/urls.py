"""URL config
----------

URL patterns of the django-helmholtz-aai to be included via::

    from django.urls import include, path

    urlpatters = [
        path("helmholtz-aai/", include("django_helmholtz_aai.urls")),
    ]
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


from django.urls import path

from django_helmholtz_aai import views

#: App name for the django-helmholtz-aai to be used in calls to
#: :func:`django.urls.reverse`
app_name = "django_helmholtz_aai"

#: urlpattern for the Helmholtz AAI
urlpatterns = [
    path("login/", views.HelmholtzLoginView.as_view(), name="login"),
    path("auth/", views.HelmholtzAuthentificationView.as_view(), name="auth"),
]
