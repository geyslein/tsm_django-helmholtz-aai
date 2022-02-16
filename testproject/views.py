from django.dispatch import receiver
from django.shortcuts import render

from django_helmholtz_aai import signals


def home(request):

    return render(request, "home.html")


@receiver(signals.aai_user_created)
def created_user(sender, user, **kwargs):
    print(f"User created: {user}")


@receiver(signals.aai_user_logged_in)
def logged_in(sender, user, **kwargs):
    print(f"User logged in: {user}")


@receiver(signals.aai_user_updated)
def user_updated(sender, user, **kwargs):
    print(f"Updated user: {user}")


@receiver(signals.aai_vo_created)
def vo_created(sender, vo, **kwargs):
    print(f"Created VO {vo}")


@receiver(signals.aai_vo_entered)
def vo_entered(sender, vo, user, **kwargs):
    print(f"User {user} entered VO {vo}")


@receiver(signals.aai_vo_left)
def vo_left(sender, vo, user, **kwargs):
    print(f"User {user} left VO {vo}")
