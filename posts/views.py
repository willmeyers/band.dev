from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from pydantic import ValidationError

from band_dev.utils import flatten_querydict
from band_dev.decorators import require_request_blog
from posts.schemas import CreatePostRequestBody, UpdatePostRequestBody, AudioUploadRequestBody
from posts.services import create_post, update_post, get_post_by_id, get_blog_post_by_link


def trending_view(request):
    return render(
        request=request,
        template_name="posts/trending.html",
        context={}
    )


@login_required
def create_view(request):
    initial_content_metadata = f"---\ntitle:\n---\n"

    if request.method == "POST":
        query_dict = flatten_querydict(request.POST)
        query_dict["user_id"] = request.user.id
        query_dict["blog_id"] = request.user.blog.id

        is_draft = "save_as_draft" in query_dict

        create_post_request = CreatePostRequestBody(**query_dict)

        uploads = []
        uploaded_files = request.FILES.getlist("audio_files")
        for file in uploaded_files:
            upload_audio_request = AudioUploadRequestBody(
                user_id=request.user.id,
                file_name=file.name,
                content_type=file.content_type,
                size=file.size,
                file=file
            )

            uploads.append(upload_audio_request)

        post = create_post(request_body=create_post_request, request_files=uploads, is_draft=is_draft)

        if is_draft:
            return redirect(reverse("posts:edit", kwargs={"post_readable_id": post.readable_id}))

        return redirect(reverse("posts:detail", kwargs={"post_readable_id": post.readable_id}))

    return render(
        request=request,
        template_name="posts/create.html",
        context={
            "initial_content_metadata": initial_content_metadata
        }
    )


@login_required
def edit_view(request, post_readable_id: str):
    post = get_post_by_id(readable_id=post_readable_id)
    post_uploads = post.uploads.all()

    if request.method == "POST":
        query_dict = flatten_querydict(request.POST)
        query_dict["post_id"] = post.id

        is_draft = "save_as_draft" in query_dict

        update_post_request = UpdatePostRequestBody(**query_dict)
        uploads = []
        uploaded_files = request.FILES.getlist("audio_files")
        for file in uploaded_files:
            upload_audio_request = AudioUploadRequestBody(
                user_id=request.user.id,
                file_name=file.name,
                content_type=file.content_type,
                size=file.size,
                file=file
            )

            uploads.append(upload_audio_request)

        post = update_post(post=post, request_body=update_post_request, request_files=uploads, is_draft=is_draft)

        if is_draft:
            return redirect(reverse("posts:edit", kwargs={"post_readable_id": post.readable_id}))

        return redirect(reverse("posts:detail", kwargs={"post_readable_id": post.readable_id}))

    return render(
        request=request,
        template_name="posts/edit_post.html",
        context={
            "post": post,
            "post_uploads": post_uploads
        }
    )


@require_request_blog()
def detail_view(request, link: str):
    post = get_blog_post_by_link(blog=request.blog, link=link)
    audio_uploads = post.uploads.all()
    uploads = []
    for upload in audio_uploads:
        url = default_storage.url(upload.file.name)
        uploads.append({
            "id": upload.id,
            "content_type": upload.content_type,
            "url": url
        })

    return render(
        request=request,
        template_name="posts/post_detail.html",
        context={
            "blog": post.blog,
            "post": post,
            "audio_uploads": uploads
        }
    )
