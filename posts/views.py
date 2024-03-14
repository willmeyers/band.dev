from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from pydantic import ValidationError

from band_dev.utils import flatten_querydict
from band_dev.decorators import require_request_blog
from posts.schemas import (
    CreatePostRequestBody,
    UpdatePostRequestBody,
    AudioUploadRequestBody,
)
from posts.services import (
    create_post,
    update_post,
    get_post_by_id,
    get_blog_post_by_link,
    delete_post
)


def trending_view(request):
    return render(request=request, template_name="posts/trending.html", context={})


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
                file=file,
            )

            uploads.append(upload_audio_request)

        post = create_post(
            request_body=create_post_request, request_files=uploads, is_draft=is_draft
        )

        if is_draft:
            return redirect(
                reverse(
                    "authusers:edit_post", kwargs={"post_readable_id": post.readable_id}
                )
            )

        return redirect(reverse("blogs:view_post", kwargs={"link": post.link}))

    return render(
        request=request,
        template_name="posts/create.html",
        context={"initial_content_metadata": initial_content_metadata},
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
                file=file,
            )

            uploads.append(upload_audio_request)

        post = update_post(
            post=post,
            request_body=update_post_request,
            request_files=uploads,
            is_draft=is_draft,
        )

        return redirect(
            reverse("authusers:edit_post", kwargs={"post_readable_id": post.readable_id})
        )

    return render(
        request=request,
        template_name="posts/edit_post.html",
        context={"post": post, "post_uploads": post_uploads},
    )


@require_http_methods(["GET"])
@login_required
def delete_view(request, post_readable_id: str):
    delete_post(readable_id=post_readable_id)

    return redirect(reverse("authusers:posts_dashboard"))
