from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from band_dev.decorators import require_request_blog
from blogs.services import get_blog, get_user_blog


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
        template_name="blogs/list_blog_posts.html",
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
        template_name="blogs/list_blog_uploads.html",
        context={"blog": blog, "uploads": uploads},
    )


@require_request_blog()
def blog_list_tags_view(request):
    blog = request.blog
    posts = blog.posts.all()

    return render(
        request=request,
        template_name="posts/list_blog_posts.html",
        context={"blog": blog, "posts": posts},
    )


@require_request_blog()
def blog_list_posts_with_tag_view(request):
    blog = request.blog
    posts = blog.posts.all()

    return render(
        request=request,
        template_name="posts/list_blog_posts.html",
        context={"blog": blog, "posts": posts},
    )
