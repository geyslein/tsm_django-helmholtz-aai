from django.urls import path

from django_helmholtz_aai import views

app_name = "django_helmholtz_aai"

urlpatterns = [
    # path('', views.home),
    path("login/", views.login, name="login"),
    path("auth/", views.HelmholtzAuthentificationView.as_view(), name="auth"),
    # path('logout/', views.logout),
]
