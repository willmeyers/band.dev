from blogs.models import Blog


def get_default_blog_metadata(blog: Blog) -> dict:
    user = blog.user

    return {
        "title": f"{blog.user.slug}'s Blog",
        "subdomain": blog.user.slug,
    }
