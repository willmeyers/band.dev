import re

from django.db import models
from django.conf import settings
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

    user = models.OneToOneField(
        "authusers.AuthUser", on_delete=models.CASCADE, related_name="blog"
    )
    sites = models.ManyToManyField(Site)

    def get_content_metadata_yaml_str(self) -> str:
        markdown.convert(self.content)
        metdata = markdown.Meta

        if self.title:
            metdata["title"] = self.title

        metdata["band_domain"] = self.domain

        metadata_yaml_str = "---\n"
        for key, value in metdata.items():
            metadata_yaml_str += f"{key}: {value}\n"
        metadata_yaml_str += "---"

        return metadata_yaml_str

    def get_stripped_content(self) -> str:
        stripped_content = re.sub(r"^---(.*?)---", "", self.content, flags=re.DOTALL)
        stripped_content = stripped_content.strip()

        return stripped_content

    def create_internal_site(self, name):
        site = Site.objects.create(
            name=name + "__internal", domain=f"{name}.{settings.SITE_DOMAIN}"
        )

        self.sites.add(site)

    @cached_property
    def domain(self) -> str:
        blog_sites = self.sites.values("name", "domain")

        subdomain = None
        custom_domain = None

        for site in blog_sites:
            if site["name"].endswith("__internal"):
                subdomain = site["domain"]
            else:
                custom_domain = site["domain"]

        domain = custom_domain if custom_domain else subdomain

        return domain

    @cached_property
    def href(self) -> str:
        scheme = "https" if settings.SITE_URL_USE_SSL else "http"

        return f"{scheme}://{self.domain}"
