from functools import wraps
from django.shortcuts import redirect
from .models import Article
from django.core.exceptions import PermissionDenied


def check_owner_or_admin(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        user = request.user
        article = Article.objects.get(pk=kwargs['article_id'])
        if article.author == user or user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
