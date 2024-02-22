from django.shortcuts import render

from blogs.services import list_blogs
from posts.services import list_post_uploads, list_posts


def home_view(request):
    if request.blog:
        return render(
            request=request,
            template_name="blogs/blog_detail.html",
            context={
                "blog": request.blog
            }
        )

    return render(
        request=request,
        template_name="home.html",
        context={}
    )


def about_upgrading_view(request):
    return render(
        request=request,
        template_name="about_upgrading.html",
        context={}
    )


def discover_view(request):
    blogs = list_blogs()
    posts = list_posts()
    post_uploads = list_post_uploads()

    return render(
        request=request,
        template_name="discover.html",
        context={
            "blogs": blogs,
            "posts": posts,
            "post_uploads": post_uploads
        }
    )
