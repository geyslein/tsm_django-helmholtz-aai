# Changelog

## v0.1.5: Patch for HELHOLTZ_MAP_ACCOUNTS and Group names

This patch makes sure that the attributes persist when a user is mapped with
`HELMHOLTZ_MAP_ACCOUNTS`, and it only changes the display name if it changed
compared to the Helmholtz AAI identifier.

## v0.1.4: Use correct setting variable for HELMHOLTZ_UPDATE_USERNAME

This patch corrects a minor issue where the `HELMHOLTZ_UPDATE_USERNAME` has not
been read correctly from the django settings.

## v0.1.3: Use case-insensitive check for email

This patch compares emails case-insensitive, see
[!7](https://gitlab.hzdr.de/hcdc/django/django-helmholtz-aai/-/merge_requests/7)
and adds a more verbose reason for the user when he or she cannot login, see
[!8](https://gitlab.hzdr.de/hcdc/django/django-helmholtz-aai/-/merge_requests/8)

## v0.1.2: Add missing migration script

This patch adds a migration script to update the manager of the HelmholtzUser and HelmholtzVirtualOrganization.
We now use the same manager as Djangos built-in user and Group.

## v0.1.1: add the HELMHOLTZ_CREATE_USERS setting

This patch adds another setting to prevent the creation of new users.
See [!6](https://gitlab.hzdr.de/hcdc/django/django-helmholtz-aai/-/merge_requests/6)


## v0.1.0: django-helmholtz-aai

Initial release of the django-helmholtz-aai package. A generic app to connect
a django project with the Helmholtz AAI.
