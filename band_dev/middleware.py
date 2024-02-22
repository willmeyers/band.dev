from django.utils.deprecation import MiddlewareMixin
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

from blogs.models import Blog


PROTECTED_SITES = ["band.local:8000", "example.com"]


class CurrentSiteMiddleware(MiddlewareMixin):
    """
    Middleware that sets `site` attribute to request object.
    """

    def process_request(self, request):
        try:
            request.site = get_current_site(request)
        except Site.DoesNotExist:
            # In the event the site does not exist, thre request's host is of the main web application.
            # We set the site to None to signifiy this.
            request.site = None


class CurrentBlogMiddleware:
    """
    Middleware that sets the `blog` attribute to a request object.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, "blog", None)

        current_site = request.site
        if current_site and current_site not in PROTECTED_SITES:
            blog = Blog.objects.filter(sites__in=[current_site]).first()
            setattr(request, "blog", blog)

        response = self.get_response(request)

        return response
