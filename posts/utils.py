from django.utils.text import slugify


def generate_post_link_from_title(title: str) -> str:
    return slugify(title)
