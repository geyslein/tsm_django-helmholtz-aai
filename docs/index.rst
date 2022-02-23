.. django-helmholtz-aai documentation master file, created by
   sphinx-quickstart on Mon Feb 21 15:15:53 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-helmholtz-aai's documentation!
================================================


This small generic Django app helps you connect to the Helmholtz AAI and make
use of it's virtual organizations.

Features
--------
Features include

- ready-to-use views for authentification against the Helmholtz AAI
- a new :class:`HelmholtzUser` class based upon djangos
  :class:`~django.contrib.auth.models.User` model and derived from the Helmholtz AAI
- a new :class:`HelmholtzVirtualOrganization` class based upon djangos
  :class:`~django.contrib.auth.models.Group` model and derived from the Helmholtz AAI
- several signals to handle the login of Helmholtz AAI user for your specific
  application
- automated synchronization of VOs of on user authentification

Get started by following the :ref:`installation instructions <installation>`
and have a look into the :ref:`configuration`.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   configuration
   common-problems
   api
   contributing



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
