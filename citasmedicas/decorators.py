from django.core.exceptions import PermissionDenied
from citasmedicas import models as m
from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            logout(request)
            return redirect("citasmedicas:login")

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
