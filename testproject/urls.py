"""django_psql_dag_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from testproject import views


class PatchRedirectView(RedirectView):
    """Patched redirect view to avoid issues with FORCE_SCRIPT_NAME"""

    def get_redirect_url(self, *args, **kwargs):
        ret = self.request.path[1:]
        script_name = settings.FORCE_SCRIPT_NAME[1:]
        while ret.startswith(script_name):
            ret = ret[len(script_name) :]
        return "/" + ret


urlpatterns = [
    path("", views.home, name="home"),
    path("", include("django.contrib.auth.urls")),
    path("helmholtz-aai/", include("django_helmholtz_aai.urls")),
    path("admin/", admin.site.urls),
]

if getattr(settings, "FORCE_SCRIPT_NAME", None):
    urlpatterns.append(
        re_path(
            settings.FORCE_SCRIPT_NAME[1:] + ".*", PatchRedirectView.as_view()
        )
    )


# # This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static("static/", document_root=settings.STATIC_ROOT)
