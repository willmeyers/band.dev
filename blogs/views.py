from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

from band_dev.decorators import require_request_blog
from blogs.services import get_blog, get_user_blog
from posts.services import get_blog_post_by_link


def discover_view(request):
    return render(request=request, template_name="blogs/discover.html", context={})


@login_required
def blog_settings_view(request):
    blog = get_user_blog(user=request.user)

    return render(
        request=request, template_name="blogs/settings.html", context={"blog": blog}
    )


def blog_detail_view(request, user_slug: str):
    blog = get_blog(user__slug=user_slug)
    posts = blog.posts.all()

    return render(
        request=request,
        template_name="blogs/blog_detail.html",
        context={"blog": blog, "posts": posts},
    )


@require_request_blog()
def blog_list_posts_view(request):
    blog = request.blog
    posts = blog.posts.all()

    return render(
        request=request,
        template_name="blogs/post_list.html",
        context={"blog": blog, "posts": posts},
    )


@require_request_blog()
def blog_list_uploads_view(request):
    blog = request.blog
    user = blog.user
    posts = blog.posts.all()
    uploads = user.uploads.all()

    return render(
        request=request,
        template_name="blogs/upload_list.html",
        context={"blog": blog, "uploads": uploads},
    )


@require_request_blog()
def blog_list_tags_view(request):
    blog = request.blog
    posts = blog.posts.all()

    return render(
        request=request,
        template_name="posts/tag_list.html",
        context={"blog": blog, "posts": posts},
    )


@require_request_blog()
def blog_list_posts_with_tag_view(request):
    blog = request.blog
    posts = blog.posts.all()

    return render(
        request=request,
        template_name="posts/post_list.html",
        context={"blog": blog, "posts": posts},
    )


@require_request_blog()
def blog_post_detail_view(request, link: str):
    post = get_blog_post_by_link(blog=request.blog, link=link)
    audio_uploads = post.uploads.all()
    uploads = []
    for upload in audio_uploads:
        url = default_storage.url(upload.file.name)
        uploads.append(
            {"id": upload.id, "content_type": upload.content_type, "url": url}
        )

    return render(
        request=request,
        template_name="blogs/post_detail.html",
        context={"blog": post.blog, "post": post, "audio_uploads": uploads},
    )
