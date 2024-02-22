from django.db import models
from django.contrib.sites.models import Site
from django.utils.functional import cached_property

from band_dev.markdown import markdown
from band_dev.models import BaseModel


class Blog(BaseModel):
    content = models.TextField(default="---\ntitle: My Music\n---\n")
    html = models.TextField(null=True)

    title = models.TextField(default="My Music")
    lang = models.TextField(default="en")
    meta_description = models.TextField(null=True)
    meta_image = models.URLField(null=True)

    # Themeing
    navbar = models.TextField(null=True)
    custom_styles = models.TextField(null=True)
    custom_music_player_styles = models.TextField(null=True)

    # Moderation
    is_blocked = models.BooleanField(default=False)
    is_discoverable = models.BooleanField(default=False)

    user = models.OneToOneField("authusers.AuthUser", on_delete=models.CASCADE, related_name="blog")
    sites = models.ManyToManyField(Site)

    def create_internal_site(self, name):
        site = Site.objects.create(
            name=name + "__internal",
            domain=f"{name}.band.local"
        )

        self.sites.add(site)

    @cached_property
    def navbar_html(self):
        navbar_document = markdown.convert(self.navbar)

        return navbar_document

    @cached_property
    def domain(self) -> str:
        scheme = "http"
        blog_sites = self.sites.values("name", "domain")

        subdomain = None
        custom_domain = None

        for site in blog_sites:
            if site["name"].endswith("__internal"):
                subdomain = site["domain"]
            else:
                custom_domain = site["domain"]

        domain = custom_domain if custom_domain else subdomain

        return f"{scheme}://{domain}:8000"
