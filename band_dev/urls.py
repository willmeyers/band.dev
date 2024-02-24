"""
URL configuration for band_dev project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import band_dev.views as home_views
import authusers.views as authusers_views
import posts.views as post_views
import blogs.views as blog_views


banddev_urls = [
    path("", home_views.home_view, name="home"),
    path("upgrade/", home_views.about_upgrading_view, name="about_upgrading"),
    path("discover", home_views.discover_view, name="discover"),
]

authusers_urls = [
    path("login/", authusers_views.login_view, name="login"),
    path("signup/", authusers_views.signup_view, name="signup"),
    path("logout/", authusers_views.logout_view, name="logout"),
    path(
        "dashboard/subscribers/",
        authusers_views.subscribers_dashboard_view,
        name="subscribers_dashboard",
    ),
    path(
        "dashboard/uploads/",
        authusers_views.post_uploads_dashboard_view,
        name="post_uploads_dashboard",
    ),
    path(
        "dashboard/posts/", authusers_views.posts_dashboard_view, name="posts_dashboard"
    ),
    path(
        "dashboard/theme/", authusers_views.theme_dashboard_view, name="theme_dashboard"
    ),
    path("dashboard/", authusers_views.dashboard_view, name="dashboard"),
    path(
        "settings/", authusers_views.settings_dashboard_view, name="settings_dashboard"
    ),
    # Posts
    path("posts/new/", post_views.create_view, name="create_post"),
    path("posts/<str:post_readable_id>/edit/", post_views.edit_view, name="edit_post"),
]

blog_urls = [
    path("posts/<str:link>", post_views.detail_view, name="view_post"),
    path("posts/", blog_views.blog_list_posts_view, name="list"),
    path("uploads/", blog_views.blog_list_uploads_view, name="list_uploads"),
    path("tags/", blog_views.blog_list_tags_view, name="list_tags"),
    path(
        "tags/<str:tag_name>/",
        blog_views.blog_list_posts_with_tag_view,
        name="list_with_tag",
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(banddev_urls)),
    path("", include((authusers_urls, "authusers"))),
    path("", include((blog_urls, "blogs"))),
]
