from typing import Optional
from functools import wraps

from django.http import HttpResponseNotFound


def require_request_blog():
    """
    Decorator to make a view only available if the request comes from a blog site.  Usage::

        @require_request_blog()
        def my_view(request):
            # I can assume now that only requests with a blog make it this far
            # ...

    Ensure CurrentBlogMiddleware is added to settings.MIDDLEWARES.
    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.blog is None:
                response = HttpResponseNotFound(*args, **kwargs)
                return response
            return func(request, *args, **kwargs)
        return inner
    return decorator
