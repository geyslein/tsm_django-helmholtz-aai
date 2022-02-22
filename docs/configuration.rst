.. _configuration:

Configuration options
=====================

Configuration settings
----------------------

Most important settings
^^^^^^^^^^^^^^^^^^^^^^^

.. automodulesumm:: django_helmholtz_aai.app_settings
    :autosummary-no-titles:
    :autosummary-members: HELMHOLTZ_CLIENT_ID, HELMHOLTZ_CLIENT_SECRET,HELMHOLTZ_ALLOWED_VOS

Two settings are necessary to use this package, this is the
:setting:`HELMHOLTZ_CLIENT_ID` and the :setting:`HELMHOLTZ_CLIENT_SECRET` that
you specified during the OAuth-Client registration (see :ref:`register-client`).

By default, the website allows all users to login and create an account via the
Helmholtz AAI. This if often not desired and you can modify this with the
:setting:`HELMHOLTZ_ALLOWED_VOS` setting, e.g. something like::

    HELMHOLTZ_ALLOWED_VOS = [
        "urn:geant:helmholtz.de:group:hereon#login.helmholtz.de",
    ]

in your ``settings.py``.

Other settings
^^^^^^^^^^^^^^

Further settings can be used to specify how to connect to the helmholtz AAI and
how to interpret the userinfo of the Helmholtz AAI.

.. automodulesumm:: django_helmholtz_aai.app_settings
    :autosummary-no-titles:
    :autosummary-exclude-members: HELMHOLTZ_CLIENT_ID, HELMHOLTZ_CLIENT_SECRET,HELMHOLTZ_ALLOWED_VOS


Customizing the login
---------------------

If you are using the Helmholtz AAI, you likely want to combine it with the
permission system of your Django project. You may want to set the `is_staff`
attribute for users of a specific VO, or perform additional actions when a
user logged in for the first time (e.g. send a welcome mail), enters or leaves
a VO.

To perfectly adjust the django-helmholtz-aai framework to your projects need,
you have two choices:

1. connect to the signals of the :mod:`~django_helmholtz_aai.signals` module,
   see :ref:`configure-signals`
2. subclass the
   :class:`~django_helmholtz_aai.views.HelmholtzAuthentificationView` view,
   see :ref:`custom-view`

The signals are the recommended way as they provide a more stable interface.
As the `django-helmholtz-aai` is very new, we cannot guarantee that there
won't be breaking changes in the
:class:`~django_helmholtz_aai.views.HelmholtzAuthentificationView`.


.. _configure-signals:

Configuration via Signals
^^^^^^^^^^^^^^^^^^^^^^^^^

The :mod:`~django_helmholtz_aai.signals` module defines various signal that are
fired on different events:

.. automodulesumm:: django_helmholtz_aai.signals
    :autosummary-no-titles:
    :autosummary-imported-members:
    :autosummary-exclude-members: Signal

The purpose of these signals should be pretty much self-explanatory.

Examples
~~~~~~~~
Suppose you want users of a specific VO to become superusers. Then you can do
something like this using the :signal:`aai_vo_entered` and
:signal:`aai_vo_left` signals::

    from django.dispatch import receiver

    from django_helmholtz_aai import models, signals

    @receiver(signals.aai_vo_entered)
    def on_vo_enter(
            sender,
            vo: models.HelmholtzVirtualOrganization,
            user: models.HelmholtzUser,
            **kwargs,
        ):
        vo_id = "urn:geant:helmholtz.de:group:hereon#login.helmholtz.de"
        if vo.eduperson_entitlement == vo_id:
            user.is_superuser = True
            user.save()


    @receiver(signals.aai_vo_left)
    def on_vo_leave(
            sender,
            vo: models.HelmholtzVirtualOrganization,
            user: models.HelmholtzUser,
            **kwargs,
        ):
        vo_id = "urn:geant:helmholtz.de:group:hereon#login.helmholtz.de"
        if vo.eduperson_entitlement == vo_id:
            user.is_superuser = False
            user.save()

Let's say you want to display a message in the frontend when a user logged in
for the first time. Here you can use the :signal:`aai_user_created` signal::

    from django.contrib import messages

    from django_helmholtz_aai import models, signals

    @receiver(signals.aai_user_created)
    def created_user(
        sender,
        user: models.HelmholtzUser,
        request,
        **kwargs,
    ):
        messages.add_message(
            request, messages.success, f"Welcome on board {user}!"
        )

.. _custom-view:

Customization via the ``HelmholtzAuthentificationView``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

    Please bear in mind that this python package is still very new and we
    cannot guarantee that there won't be breaking changes in the
    :class:`~django_helmholtz_aai.views.HelmholtzAuthentificationView` class.

Another way to customize the login is via the
:class:`~django_helmholtz_aai.views.HelmholtzAuthentificationView`. Your
starting point should be the following two methods, one for checking the
permissions and one for performing the request:

.. autoclasssumm:: django_helmholtz_aai.views.HelmholtzAuthentificationView
    :autosummary-no-titles:
    :autosummary-members: get, has_permission

For a more fine-grained control of the authentification (such as user creation
or update), you can make use of the following methods and reimplement to your
needs.

.. autoclasssumm:: django_helmholtz_aai.views.HelmholtzAuthentificationView
    :autosummary-no-titles:
    :autosummary-members: create_user, update_user, login_user, synchronize_vos
    :autosummary-sections: Methods


Example
~~~~~~~

Let's say you want to approve users before you let them login to the website.
One possibility is, to create a custom model with reference to a user and
reimplement the
:meth:`django_helmholtz_aai.views.HelmholtzAuthentificationView.login_user`.
Your custom app that reimplements this view then might look like

- ``models.py``

  .. code-block:: python

      from django.db import models
      from django_helmholtz_aai.models import HelmholtzUser


      class HelmholtzUserReview(models.Model):
          """A review of a helmholtz user"""

          class ReviewStatus(models.TextChoices):

              accepted = "accepted"
              rejected = "rejected"

          user = models.OneToOneField(HelmholtzUser, on_delete=models.CASCADE)

          review_status = models.CharField(
              choices=ReviewStatus.choices, blank=True, null=True
          )

- ``views.py``

  .. code-block:: python

      from django.contrib import messages
      from django_helmholtz_aai.views import HelmholtzAuthentificationView
      from django_helmholtz_aai.models import HelmholtzUser
      from .models import HelmholtzUserReview


      class CustomHelmholtzAuthentificationView(HelmholtzAuthentificationView):
          def login_user(self, user: HelmholtzUser):
              review = HelmholtzUserReview.objects.get_or_create(user=user)[0]
              if (
                  review.review_status
                  == HelmholtzUserReview.ReviewStatus.accepted
              ):
                  super().login_user(user)
              elif (
                  review.review_status
                  == HelmholtzUserReview.ReviewStatus.rejected
              ):
                  messages.add_message(
                      self.request,
                      messages.error,
                      f"Your account creation request has been rejected.",
                  )
              else:
                  messages.add_message(
                      self.request,
                      messages.success,
                      f"Your account creation request is currently under review.",
                  )

- ``urls.py``

  .. code-block:: python

      from django.urls import include, path
      from .views import CustomHelmholtzAuthentificationView

      urlpatterns = [
          path(
              "helmholtz-aai/auth/",
              CustomHelmholtzAuthentificationView.as_view(),
          ),
          path("helmholtz-aai/", include("django_helmholtz_aai.urls")),
      ]
