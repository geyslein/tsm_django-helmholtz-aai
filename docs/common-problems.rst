.. _common-problems:

Common problems
===============

In this document, we collect common problems and questions. If you cannot find
your issue documented in here, you should
`create an issue at the source code repository`_ and we'll try to find a solution and update this
document with your problem.

.. _create an issue at the source code repository: https://gitlab.hzdr.de/hcdc/django/django-helmholtz-aai/issues/new/

Mapping to existing accounts
----------------------------
When you add this app to an existing django project, you might already have
accounts in your database. If this is the case, you should have a look into
the :setting:`HELMHOLTZ_MAP_ACCOUNTS` configuration variable.

Mapping of multiple accounts
----------------------------
One user can have multiple accounts in the Helmholtz AAI. You can, for
instance create an account via GitHub and through your home institution.
Both accounts can have the same email address. The Helmholtz AAI however
treats them as separate accounts and both have different unique IDs and
belong to different VOs. As we use the ID for mapping a user in the
Helmholtz AAI to a user in Django, and we synchronize the VOs of the
user in the Helmholtz AAI, we have to distinguish the two accounts as well.

As an example: One user can register two accounts in the Helmholtz AAI:

1. one via Google
2. one via GitHub but with the same Google-Mail

Then the user logs in to your project via the Helmholtz AAI and his Google
account. If the user then logs in to your project via GitHub, this creates
a new account, independent from the first one.

Usually you do not want to have this behaviour as both user-accounts will
then have the same email-address. Therefore this is disabled by default.
However, you can allow the creation of multiple user accounts using the
:setting:`HELMHOLTZ_EMAIL_DUPLICATES_ALLOWED` configuration variable.

Too many VOs
------------
Each time a user account is created, we create the VOs that the user
participates in. These VOs remain, even if one deletes the user account. To
remove these empty VOs, we therefore added the
:mod:`~django_helmholtz_aai.management.commands.remove_empty_vos` management
command that you can use via ``python manage.py remove_empty_vos``. Or you call
it directly from python, e.g. via::

    from django_helmholtz_aai import models
    models.HelmholtzVirtualOrganization.objects.remove_empty_vos()
