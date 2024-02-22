from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from band_dev.utils import flatten_querydict
from authusers.services import create_user, authenticate_user, get_user, update_user_settings
from authusers.schemas import CreateUserRequestBody, AuthenticateUserRequestBody, SettingsRequestBody
from blogs.schemas import UpdateBlogRequestBody
from blogs.services import update_user_blog
from posts.services import get_user_posts


def signup_view(request):
    if request.method == "POST":
        query_dict = {k: request.POST.get(k) for k in request.POST}
        create_user_request = CreateUserRequestBody(**query_dict)

        user = create_user(request_body=create_user_request)

        login(request=request, user=user)

    return render(request, "authusers/signup.html", {})


def login_view(request):
    if request.method == "POST":
        query_dict = {k: request.POST.get(k) for k in request.POST}
        login_request = AuthenticateUserRequestBody(**query_dict)

        try:
            user = authenticate_user(request_body=login_request)
            login(request=request, user=user)

            return redirect("/")
        except:
            pass

    return render(request, "authusers/login.html", {})


@login_required
def logout_view(request):
    logout(request=request)

    return redirect("/")


@login_required
def dashboard_view(request):
    blog = request.user.blog

    if request.method == "POST":
        query_dict = flatten_querydict(querydict=request.POST)
        update_blog_request = UpdateBlogRequestBody(**query_dict)
        blog = update_user_blog(blog=blog, request_body=update_blog_request)

    return render(
        request=request,
        template_name="authusers/dashboard.html",
        context={
            "user": request.user,
            "blog": blog,
        }
    )


@login_required
def subscribers_dashboard_view(request):
    return render(
        request=request,
        template_name="authusers/subscribers_dashboard.html",
        context={
            "user": request.user,
            "blog": request.user.blog,
        }
    )


@login_required
def posts_dashboard_view(request):
    return render(
        request=request,
        template_name="authusers/posts_dashboard.html",
        context={
            "user": request.user,
            "blog": request.user.blog,
            "posts": request.user.blog.posts.all()
        }
    )


@login_required
def post_uploads_dashboard_view(request):
    user = request.user,
    blog = request.user.blog,
    posts = request.user.posts.all()
    post_uploads = request.user.uploads.all()

    return render(
        request=request,
        template_name="authusers/post_uploads_dashboard.html",
        context={
            "user": user,
            "blog": blog,
            "posts": posts,
            "post_uploads": post_uploads
        }
    )


@login_required
def theme_dashboard_view(request):
    return render(
        request=request,
        template_name="authusers/theme_dashboard.html",
        context={
            "user": request.user,
            "blog": request.user.blog,
        }
    )


@login_required
def settings_dashboard_view(request):
    user = request.user

    if request.method == "POST":
        query_dict = {k: request.POST.get(k) for k in request.POST}
        settings_request = SettingsRequestBody(**query_dict)

        user = update_user_settings(user=user, request_body=settings_request)

    return render(
        request=request,
        template_name="authusers/settings_dashboard.html",
        context={
            "user": user,
            "blog": user.blog,
        }
    )
