import re

from django.db import transaction
from django.db.models import F, QuerySet
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from band_dev.utils import decode_readable_id
from band_dev.markdown import markdown
from authusers.models import AuthUser
from blogs.models import Blog
from posts.models import Post, PostUpload
from posts.schemas import CreatePostRequestBody, UpdatePostRequestBody, AudioUploadRequestBody
from posts.utils import generate_post_link_from_title


@transaction.atomic
def create_post(request_body: CreatePostRequestBody, request_files: list[AudioUploadRequestBody], is_draft: bool = False) -> Post:
    document = markdown.convert(request_body.content)
    metadata = markdown.Meta

    post = Post(
        is_draft=is_draft,
        user_id=request_body.user_id,
        blog_id=request_body.blog_id,
    )

    post.content = request_body.content
    post.html = document

    post.title = metadata.get("title")
    post.link = metadata.get("link", generate_post_link_from_title(title=post.title))
    post.meta_image = metadata.get("meta_image")
    post.meta_description = metadata.get("meta_description")
    post.tags = metadata.get("tags")
    post.class_name = metadata.get("class_name")
    post.is_discoverable = metadata.get("is_discoverable", True)
    post.is_page = metadata.get("is_page", False)

    post.save()

    if len(request_files) > 12:
        raise ValueError("too many files")

    for request_file in request_files:
        create_upload_audio(post=post, request_body=request_file)

    return post


@transaction.atomic
def update_post(post: Post, request_body: UpdatePostRequestBody, request_files: list[AudioUploadRequestBody], is_draft: bool = False) -> Post:
    document = markdown.convert(request_body.content)
    metadata = markdown.Meta

    post.content = request_body.content
    post.html = document

    post.title = metadata.get("title")
    post.link = metadata.get("link", generate_post_link_from_title(title=post.title))
    post.meta_image = metadata.get("meta_image")
    post.meta_description = metadata.get("meta_description")
    post.tags = metadata.get("tags")
    post.class_name = metadata.get("class_name")
    post.is_discoverable = metadata.get("is_discoverable", True)
    post.is_page = metadata.get("is_page", False)

    post.content = post.get_content_metadata_yaml_str() + post.get_stripped_content()

    post.save()

    if len(request_files) > 12:
        raise ValueError("too many files")

    for request_file in request_files:
        create_upload_audio(post=post, request_body=request_file)

    return post



def create_upload_audio(post: Post, request_body: AudioUploadRequestBody) -> PostUpload:
    # TODO: ensure safe string building
    file_name = default_storage.save(f"user_media/{request_body.user_id}/audio/{request_body.file_name}", ContentFile(request_body.file.read()))
    post_upload = PostUpload(
        post_id=post.id,
        user_id=request_body.user_id,
        file=file_name,
        content_type=request_body.content_type
    )
    post_upload.save()

    return post_upload


def get_post_by_id(readable_id: str) -> Post:
    valid, id = decode_readable_id(readable_id=readable_id)

    post = Post.objects.get(id=id)

    return post


def get_blog_post_by_link(blog: Blog, link: str) -> Post:
    post = Post.objects.get(blog=blog, link=link)

    return post


def get_user_posts(user: AuthUser) -> QuerySet[Post]:
    queryset = Post.objects.filter(user=user)

    return queryset


def list_posts() -> QuerySet[Post]:
    posts = Post.objects.filter()

    return posts


def list_post_uploads() -> QuerySet[PostUpload]:
    uploads = PostUpload.objects.filter()

    return uploads
