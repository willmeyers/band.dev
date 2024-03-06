import re
from typing_extensions import Literal, Optional

from django.utils.text import slugify
from django.db.models.query_utils import Q
from django.db.models.query import QuerySet
from django.template import engines
from django.template.loader import render_to_string

from band_dev.markdown import markdown
from posts.models import Post, PostUpload


VALID_CONTENT_TAG_FILTERS = ["limit", "order_by"]


VALID_POST_CONTENT_TAG_FILTERS = ["tags"]


VALID_UPLOAD_CONTENT_TAG_FILTERS = ["tags"]


def generate_post_link_from_title(title: str) -> str:
    return slugify(title)


def render_content_tag(context_key: str, template_name: str, queryset: QuerySet) -> str:
    return render_to_string(template_name=template_name, context={context_key: queryset})


def create_content_tag_filter_from_match(content_filter_match: str) -> Optional[Q]:
    try:
        key, value = content_filter_match.split(":")
    except ValueError:
        return None

    if key not in VALID_CONTENT_TAG_FILTERS:
        return None

    query = None

    match key:
        case "tags":
            query = Q(**{"tags__in": value})
        case _:
            query = None

    return query


# TODO (willmeyers): Ensure safe inserting of html from tags. Test XSS and other vulns
def render_post(post: Post) -> str:
    def replace_match_with_rendered_template(match):
        """
        Callback function used for sub'ing matches
        """
        kind = match.group(0)
        kind = kind.replace("{{", "").replace("}}", "").strip()
        filters = match.group(1)
        final_query = Q(user=post.user)
        try:
            filters = match.group(1)[1:].split("|")
            for f in filters:
                query = create_content_tag_filter_from_match(content_filter_match=f)
                final_query |= query if query else final_query
        except IndexError as err:
            print(err)
            pass

        return render_content_tag(
            context_key=kind,
            template_name=f"_partials/{kind}_list.html",
            queryset=Post.objects.filter(final_query)
        )

    template_engine = engines["django"]

    posts_pattern = r"\{\{\s*(posts|uploads|post_uploads)\s*([^}]*)\}\}"
    document = re.sub(posts_pattern, replace_match_with_rendered_template, post.content)

    document = markdown.convert(document)
    metadata = markdown.Meta

    context = {
        "blog_title": post.blog.title,
        "post_title": post.title,
    }

    document = template_engine.from_string(document).render(context=context)

    return document
