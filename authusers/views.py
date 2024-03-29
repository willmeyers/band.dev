from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from band_dev.utils import flatten_querydict
from authusers.services import (
    create_user,
    authenticate_user,
    get_user_by_id,
    activate_user_account,
    update_user_settings,
)
from authusers.schemas import (
    CreateUserRequestBody,
    AuthenticateUserRequestBody,
    SettingsRequestBody,
)
from blogs.schemas import UpdateBlogRequestBody
from blogs.services import update_user_blog
from blogs.themes import theme_map, music_player_theme_map, DEFAULT_THEME, DEFAULT_MUSIC_PLAYER_THEME
from posts.services import get_user_posts
from emails.services import send_account_activation_email_to_user


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
def send_activate_account_email(request):
    if request.user.is_verified:
        return redirect(reverse("home"))

    send_account_activation_email_to_user(user=request.user)

    return render(
        request=request,
        template_name="authusers/send_activate_account_email.html",
    )


def activate_account_view(request, readable_user_id, token):
    success = activate_user_account(readable_id=readable_user_id, token=token)
    if success:
        return redirect(reverse("authusers:dashboard"))

    return render(
        request=request,
        template_name="authusers/activate_account.html",
        context={
            "success": success
        }
    )


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
        },
    )


@login_required
def subscribers_dashboard_view(request):
    return render(
        request=request,
        template_name="authusers/subscribers_dashboard.html",
        context={
            "user": request.user,
            "blog": request.user.blog,
        },
    )


@login_required
def posts_dashboard_view(request):
    return render(
        request=request,
        template_name="authusers/posts_dashboard.html",
        context={
            "user": request.user,
            "blog": request.user.blog,
            "posts": request.user.blog.posts.all(),
        },
    )


@login_required
def post_uploads_dashboard_view(request):
    user = (request.user,)
    blog = (request.user.blog,)
    posts = request.user.posts.all()
    post_uploads = request.user.uploads.all()

    return render(
        request=request,
        template_name="authusers/post_uploads_dashboard.html",
        context={
            "user": user,
            "blog": blog,
            "posts": posts,
            "post_uploads": post_uploads,
        },
    )


@login_required
def theme_dashboard_view(request):
    user = request.user
    blog = request.user.blog

    if request.method == "POST":
        request_body = flatten_querydict(querydict=request.POST)
        # TODO (willmeyers): add proper validation for both cases
        if "apply-theme" in request_body:
            try:
                theme_name = request_body.get("theme_name")
                theme = theme_map[theme_name]
                music_player_theme = music_player_theme_map[theme_name]
            except (KeyError, ValueError):
                pass

            blog.custom_styles = theme
            blog.custom_music_player_styles = music_player_theme
            blog.save()

        if "publish-styles" in request_body:
            blog.custom_styles = request_body.get("custom_styles")
            blog.custom_music_player_styles = request_body.get("custom_music_player_styles")
            blog.save()

    custom_styles = blog.custom_styles
    if not custom_styles:
        custom_styles = DEFAULT_THEME

    custom_music_player_styles = blog.custom_music_player_styles
    if not custom_music_player_styles:
        custom_music_player_styles = DEFAULT_MUSIC_PLAYER_THEME

    return render(
        request=request,
        template_name="authusers/theme_dashboard.html",
        context={
            "user": user,
            "blog": blog,
            "custom_styles": custom_styles,
            "custom_music_player_styles": custom_music_player_styles
        },
    )


@login_required
def settings_dashboard_view(request):
    user = request.user
    blog = request.user.blog

    if request.method == "POST":
        query_dict = {k: request.POST.get(k) for k in request.POST}
        settings_request = SettingsRequestBody(**query_dict)

        user = update_user_settings(user=user, request_body=settings_request)

    return render(
        request=request,
        template_name="authusers/settings_dashboard.html",
        context={
            "user": user,
            "blog": blog,
        },
    )
