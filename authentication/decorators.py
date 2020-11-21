from functools import wraps
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:index')
        else:
            return view_func(request, *args, **kwargs)
    return wrap