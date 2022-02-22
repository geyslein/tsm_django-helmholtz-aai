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

#: Signal that is fired when a user has been created via the Helmholtz AAI
#:
#: This signal is called by the
#: :class:`~django_helmholtz_aai.views.HelmholtzAuthentificationView` when a new
#: user has been created. Subscribers to this signal can accept the following
#: parameters.
#:
#: .. signal:: aai_user_created
#:
#: Parameters
#: ----------
#: sender: Type[django_helmholtz_aai.models.HelmholtzUser]
#:     The type who sent the signal (implemented for reasons of convention)
#: user: django_helmholtz_aai.models.HelmholtzUser
#:     The new user that has been created
#: request: Request
#:     The request holding the session of the user.
#: userinfo: Dict[str, Any]
#:     The userinfo as obtained from the Helmholtz AAI
#:
#: See Also
#: --------
#: django_helmholtz_aai.views.HelmholtzAuthentificationView.create_user
aai_user_created = Signal()


#: Signal that is fired when a user logs in via the Helmholtz AAI
#:
#: This signal is called by the
#: :class:`~django_helmholtz_aai.views.HelmholtzAuthentificationView` when a
#: user logged in via the Helmholtz AAI. Subscribers to this signal can accept
#: the following parameters.
#:
#: .. signal:: aai_user_logged_in
#:
#: Parameters
#: ----------
#: sender: Type[django_helmholtz_aai.models.HelmholtzUser]
#:     The type who sent the signal (implemented for reasons of convention)
#: user: django_helmholtz_aai.models.HelmholtzUser
#:     The user who just logged in
#: request: Request
#:     The request holding the session of the user.
#: userinfo: Dict[str, Any]
#:     The userinfo as obtained from the Helmholtz AAI
#:
#: See Also
#: --------
#: django_helmholtz_aai.login
#: django_helmholtz_aai.views.HelmholtzAuthentificationView.login_user
aai_user_logged_in = Signal()


#: Signal that is fired when a user receives an update via the Helmholtz AAI
#:
#: This signal is called by the
#: :class:`~django_helmholtz_aai.views.HelmholtzAuthentificationView` when a
#: user who does already have an account gets updated, e.g. because the email
#: of the ``preferred_username`` changed in the Helmholtz AAI. Subscribers to
#: this signal can accept the following parameters.
#:
#: .. signal:: aai_user_updated
#:
#: Parameters
#: ----------
#: sender: Type[django_helmholtz_aai.models.HelmholtzUser]
#:     The type who sent the signal (implemented for reasons of convention)
#: user: django_helmholtz_aai.models.HelmholtzUser
#:     The user that is supposed to be updated
#: request: Request
#:     The request holding the session of the user.
#: userinfo: Dict[str, Any]
#:     The userinfo as obtained from the Helmholtz AAI
#:
#: See Also
#: --------
#: django_helmholtz_aai.views.HelmholtzAuthentificationView.update_user
aai_user_updated = Signal()


#: Signal that is fired if a new Virtual Organization has been created
#:
#: This signal is called by the
#: :class:`~django_helmholtz_aai.views.HelmholtzAuthentificationView` when a
#: new virtual organization has been created from the Helmholtz AAI because a
#: of this VO registered on the website. Subscribers to
#: this signal can accept the following parameters.
#:
#: .. signal:: aai_vo_created
#:
#: Parameters
#: ----------
#: sender: Type[django_helmholtz_aai.models.HelmholtzUser]
#:     The type who sent the signal (implemented for reasons of convention)
#: user: django_helmholtz_aai.models.HelmholtzUser
#:     The user that is about to become a member of the new VO
#: vo: django_helmholtz_aai.models.HelmholtzVirtualOrganization
#:     The VO that has just been created
#: request: Request
#:     The request holding the session of the user.
#: userinfo: Dict[str, Any]
#:     The userinfo as obtained from the Helmholtz AAI
#:
#: See Also
#: --------
#: django_helmholtz_aai.views.HelmholtzAuthentificationView.synchronize_vos
aai_vo_created = Signal()


#: Signal that is fired if a Helmholtz AAI user enteres a VO
#:
#: This signal is called by the
#: :class:`~django_helmholtz_aai.views.HelmholtzAuthentificationView` when a
#: user enters a virtual organization as the user is a member in the Helmholtz
#: AAI. Subscribers to this signal can accept the following parameters.
#:
#: .. signal:: aai_vo_entered
#:
#: Parameters
#: ----------
#: sender: Type[django_helmholtz_aai.models.HelmholtzUser]
#:     The type who sent the signal (implemented for reasons of convention)
#: user: django_helmholtz_aai.models.HelmholtzUser
#:     The user that entered the VO.
#: vo: django_helmholtz_aai.models.HelmholtzVirtualOrganization
#:     The VO that the user has just entered
#: request: Request
#:     The request holding the session of the user.
#: userinfo: Dict[str, Any]
#:     The userinfo as obtained from the Helmholtz AAI
#:
#: See Also
#: --------
#: django_helmholtz_aai.views.HelmholtzAuthentificationView.synchronize_vos
aai_vo_entered = Signal()


#: Signal that is fired if a Helmholtz AAI user left a VO
#:
#: This signal is called by the
#: :class:`~django_helmholtz_aai.views.HelmholtzAuthentificationView` when a
#: user leaves a virtual organization as the user is not anymore a member in
#: the Helmholtz AAI. Subscribers to this signal can accept the following
#: parameters.
#:
#: .. signal:: aai_vo_left
#:
#: Parameters
#: ----------
#: sender: Type[django_helmholtz_aai.models.HelmholtzUser]
#:     The type who sent the signal (implemented for reasons of convention)
#: user: django_helmholtz_aai.models.HelmholtzUser
#:     The user that entered the VO.
#: vo: django_helmholtz_aai.models.HelmholtzVirtualOrganization
#:     The VO that the user has just entered
#: request: Request
#:     The request holding the session of the user.
#: userinfo: Dict[str, Any]
#:     The userinfo as obtained from the Helmholtz AAI
#:
#: See Also
#: --------
#: django_helmholtz_aai.views.HelmholtzAuthentificationView.synchronize_vos
aai_vo_left = Signal()
