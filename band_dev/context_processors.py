from django.conf import settings


def global_variables(request):
    return {
        "SITE_URL": settings.SITE_URL
    }
