from functools import wraps
from django.shortcuts import redirect
from .models import Profile
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User


def unauthenticated_user(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:index')
        else:
            return view_func(request, *args, **kwargs)
    return wrap


def check_profile_owner(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        user = request.user
        profile_owner = User.objects.get(username=kwargs['username'])
        profile_owner_id = profile_owner.id
        profile = Profile.objects.get(pk=profile_owner_id)
        if profile.user == user or user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
