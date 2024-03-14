import re

from django.db import models
from django.utils.functional import cached_property
from django.core.files.storage import default_storage
from django.contrib.postgres.fields import ArrayField

from band_dev.models import BaseModel
from band_dev.markdown import markdown


class Post(BaseModel):
    title = models.TextField(null=True)
    content = models.TextField()
    html = models.TextField(null=True)
    link = models.TextField(null=True)
    published_date = models.DateTimeField(null=True)
    class_name = models.TextField(null=True)
    meta_image = models.URLField(null=True)
    meta_description = models.TextField(null=True)
    is_page = models.BooleanField(default=False)
    is_discoverable = models.BooleanField(default=True)
    is_draft = models.BooleanField(default=False)
    tags = ArrayField(models.CharField(max_length=64), size=16, null=True)
    user = models.ForeignKey(
        "authusers.AuthUser", on_delete=models.CASCADE, related_name="posts"
    )
    blog = models.ForeignKey(
        "blogs.Blog", on_delete=models.CASCADE, related_name="posts"
    )

    def get_content_metadata_yaml_str(self):
        markdown.convert(self.content)
        metdata = markdown.Meta

        if self.title:
            metdata["title"] = self.title

        if self.link:
            metdata["link"] = self.link

        if self.published_date:
            metdata["published_dat"] = self.published_date

        if self.class_name:
            metdata["class_name"] = self.class_name

        metadata_yaml_str = "---\n"
        for key, value in metdata.items():
            metadata_yaml_str += f"{key}: {value}\n"
        metadata_yaml_str += "---"

        return metadata_yaml_str

    def get_stripped_content(self):
        stripped_content = re.sub(r"^---(.*?)---", "", self.content, flags=re.DOTALL)
        stripped_content = stripped_content.strip()

        return stripped_content


class PostUpload(BaseModel):
    name = models.TextField(null=True)
    file = models.FileField()
    key = models.TextField(null=True)
    content_type = models.TextField(null=True)
    user = models.ForeignKey(
        "authusers.AuthUser", on_delete=models.CASCADE, related_name="uploads"
    )
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="uploads"
    )

    @cached_property
    def filename(self) -> str:
        return self.file.name.split("/")[-1]

    @cached_property
    def url(self) -> str:
        return default_storage.url(self.file.name)

    @cached_property
    def custom_music_player_styles(self) -> str:
        return self.post.blog.custom_music_player_styles


class Kudo(BaseModel):
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="kudos"
    )
    user = models.ForeignKey(
        "authusers.AuthUser", on_delete=models.SET_NULL, null=True, related_name="kudos"
    )
    ip_address = models.GenericIPAddressField()
