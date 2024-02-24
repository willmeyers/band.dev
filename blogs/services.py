import re
from typing import Unpack, TypedDict, Optional

from django.db.models import QuerySet
from pydantic import ValidationError

from band_dev.markdown import markdown
from authusers.models import AuthUser
from blogs.schemas import UpdateBlogRequestBody, BlogMarkdownMetadata
from blogs.models import Blog
from blogs.utils import get_default_blog_metadata


def create_user_blog(user: AuthUser) -> Blog:
    blog_title = f"{user.slug}'s Blog"

    blog = Blog.objects.create(
        user=user,
        title=blog_title,
    )

    blog.create_internal_site(name=user.slug)

    blog_metadata_yaml_str = blog.get_content_metadata_yaml_str()
    blog_stripped_content = blog.get_stripped_content()

    blog.content = blog_metadata_yaml_str + blog_stripped_content

    blog.save()

    return blog


def get_blog(**filters: Unpack[TypedDict]) -> Optional[Blog]:
    return Blog.objects.filter(**filters).first()


def get_user_blog(user: AuthUser) -> Blog:
    return Blog.objects.get(user=user)


def update_user_blog(blog: Blog, request_body: UpdateBlogRequestBody) -> Blog:
    document = markdown.convert(request_body.content)
    metadata = markdown.Meta

    # TODO (willmeyers): investigate...
    # There seems to be an odd issue when accessing markdown.Meta...
    # The previous state is somehow preserved in testcases.
    # So, we look at the document to determine if metadata is missing
    if not document:
        metadata = get_default_blog_metadata(blog=blog)

    blog_metadata = BlogMarkdownMetadata(**metadata)

    # TODO (willmeyers): handle these attribs
    # blog.subdomain = blog_metadata.subdomain
    # blog.custom_domain = blog_metadata.custom_domain

    blog.title = blog_metadata.title
    blog.meta_image = blog_metadata.meta_image
    blog.meta_description = blog_metadata.meta_description
    blog.lang = blog_metadata.lang

    blog.html = document
    blog.content = request_body.content
    blog.navbar = request_body.navbar

    if blog_metadata.band_domain:
        blog.sites.filter(name__endswith="__internal").update(
            domain=blog_metadata.band_domain
        )

    blog.save()

    return blog


def list_blogs() -> QuerySet[Blog]:
    blogs = Blog.objects.filter()

    return blogs
