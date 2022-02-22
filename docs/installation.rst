.. _installation:

Installation
============

To install the `django-helmholtz-aai` package for your Django project, you need
to follow three steps:

1. :ref:`Install the package <install-package>`
2. :ref:`Register an OAuth-client <register-client>`
3. :ref:`Add the app to your Django project <install-django-app>`

.. _install-package:

Installation from PyPi
----------------------
The recommended way to install this package is via pip and PyPi via::

    pip install django-helmholtz-aai

Or install it directly from `the source code repository on Gitlab`_ via::

    pip install git+https://gitlab.hzdr.de/hcdc/django/django-helmholtz-aai.git

The latter should however only be done if you want to access the development
versions.

.. _the source code repository on Gitlab: https://gitlab.hzdr.de/hcdc/django/django-helmholtz-aai


.. _register-client:

Register your OAuth-Client at the Helmholtz AAI
-----------------------------------------------

To install this app in your Django application, you first need to register
an OAuth client for the Helmholtz AAI. In short, this works the following way

1. head over to https://login.helmholtz.de
2. make sure that you are logged out at the Helmholtz AAI
3. click *No Acccount? Sign up* on the top-right on , and then by
4. click on *Oauth2/OIDC client Registration*
5. register your client. For more information on the necessary fields, see
   [client-registration]_ in the Helmholtz AAI docs.

   .. note::

       Make sure that you enter the correct return URL which should be
       something like
       ``https://<link-to-your-django-website>/helmholtz-aai/auth/``.

       The ``/helmholtz-aai/`` part is determined by the settings in your URL
       configuration :ref:`down below <install-django-app>`. But you can also
       change this URL or add more once your client has been approved at
       https://login.helmholtz.de/oauthhome/

.. _install-django-app:

Install the Django App for your project
---------------------------------------
To use the `django-helmholtz-aai` package in your Django project, you need to
add the app to your `INSTALLED_APPS`, configure your `urls.py`, run the
migration, add a login button in your templates. Here are the step-by-step
instructions:

1. Add the `django_helmholtz_aai` app to your `INSTALLED_APPS`
2. in your projects urlconf (see :setting:`ROOT_URLCONF`), add include
   :mod:`django_helmholtz_aai.urls` via::

       from django.urls import include, path

       urlpatterns += [
           path("helmholtz-aai/", include("django_helmholtz_aai.urls")),
        ]

   Note that the ``helmholtz-aai/``-part has to match what you entered when
   you registered your client (see :ref:`above <register-client>`).
3. Run ``python manage.py migrate`` to add the
   :class:`~django_helmholtz_aai.models.HelmholtzUser` and
   :class:`~django_helmholtz_aai.models.HelmholtzVirtualOrganization` models
   to your database
4. Add the link to the login view in one of your templates (e.g. in the
   `login.html` template from your :setting:`LOGIN_URL`), e.g. via

   .. code-block:: html

        {% load helmholtz_aai %}

        <a href="{% helmholtz_login_url %}">
          login via Helmholtz AAI
        </a>

   .. note::

        To tell the user why he or should could not login, we are also using
        djangos ``messaging`` framework. See :mod:`django.contrib.messages`.
        To display these messages, you should add something in your django
        template, e.g. something like

        .. code-block:: html

            {% if messages %}
               <ul class="messages">
                 {% for message in messages %}
                   <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>
                     {{ message }}
                   </li>
                 {% endfor %}
               </ul>
            {% endif %}

5. Make sure to set the :attr:`~django_helmholtz_aai.app_settings.HELMHOLTZ_CLIENT_ID`
   and :attr:`~django_helmholtz_aai.app_settings.HELMHOLTZ_CLIENT_SECRET`
   settings in your `settings.py` with the username and password you specified
   during the :ref:`client registration <register-client>`.

That's it! For further adaption to you Django project, please head over to the
:ref:`configuration`. You can also have a look into the ``testproject``
in the `source code repository`_ for a possible implementation.

.. _source code repository: https://gitlab.hzdr.de/hcdc/django/django-helmholtz-aai

References
----------
.. [client-registration] https://hifis.net/doc/helmholtz-aai/howto-services/
