import re
from typing import Unpack, TypedDict, Optional

from django.db.models import QuerySet
from pydantic import ValidationError

from band_dev.markdown import markdown
from authusers.models import AuthUser
from blogs.schemas import UpdateBlogRequestBody, BlogMarkdownMetadata, UpdateBlogCustomStylesRequestBody
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
    # if not document:
    #     metadata = get_default_blog_metadata(blog=blog)

    blog_metadata = BlogMarkdownMetadata(**metadata)

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

    blog_metadata_yaml_str = blog.get_content_metadata_yaml_str()
    blog_stripped_content = blog.get_stripped_content()

    blog.content = blog_metadata_yaml_str + blog_stripped_content

    blog.save()

    return blog


def update_user_blog_custom_styles(blog: Blog, request_body: UpdateBlogCustomStylesRequestBody) -> Blog:
    # TODO (willmeyers): validate CSS? Strip specific attributes?

    if request_body.reset_to_default:
        blog.custom_styles = None
        blog.custom_music_player_styles = None

    if request_body.custom_styles and not request_body.reset_to_default:
        blog.custom_styles = request_body.custom_styles

    if request_body.custom_music_player_styles and not request_body.reset_to_default:
        blog.custom_music_player_styles = request_body.custom_music_player_styles

    return blog


def list_blogs() -> QuerySet[Blog]:
    blogs = Blog.objects.filter()

    return blogs
