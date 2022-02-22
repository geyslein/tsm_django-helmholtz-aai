===============================
Django Helmholtz AAI Connection
===============================

This small generic Django app helps you connect to the Helmholtz AAI and make
use of it's virtual organizations.

Features
--------
Features include

- ready-to-use views for authentification against the Helmholtz AAI
- a new ``HelmholtzUser`` model based upon djangos ``User`` model and derived
  from the Helmholtz AAI
- a new ``HelmholtzVirtualOrganization`` model based upon djangos
  ``Group`` model and derived from the Helmholtz AAI
- several signals to handle the login of Helmholtz AAI user for your specific
  application
- automated synchronization of VOs of on user authentification

Get started by following the `installation instructions`_ and have a look into
the `configuration`_ and examples provided there.


.. _installation instructions: https://django-helmholtz-aai.readthedocs.io/en/latest/installation.html
.. _configuration: https://django-helmholtz-aai.readthedocs.io/en/latest/configuration.html


Copyright
---------
Copyright © 2021 Helmholtz-Zentrum Hereon, 2020-2021 Helmholtz-Zentrum Geesthacht

Licensed under the EUPL-1.2-or-later

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the EUPL-1.2 license for more details.

You should have received a copy of the EUPL-1.2 license along with this
program. If not, see https://www.eupl.eu/.
