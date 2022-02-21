"""Signals
-------

This module defines the signals that are fired by the views in
:mod:`django_helmholtz_aai.views` module.
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


from django.dispatch import Signal

#: Signal that is fired when a Helmholtz AAI user logs in for the first time
aai_user_created = Signal()

#: Signal that is fired when a Helmholtz AAI user logs in
aai_user_logged_in = Signal()

#: Signal that is fired when a Helmholtz AAI user logs in and is updated
aai_user_updated = Signal()

#: Signal that is fired if a new Virtual Organization has been created
aai_vo_created = Signal()

#: Signal that is fired if a Helmholtz AAI user enteres a VO
aai_vo_entered = Signal()

#: Signal that is fired if a Helmholtz AAI user left a VO
aai_vo_left = Signal()
