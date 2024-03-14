import re
from typing_extensions import Literal, Optional

from django.utils.text import slugify
from django.db.models.query_utils import Q
from django.db.models.query import QuerySet
from django.template import engines
from django.template.loader import render_to_string

from band_dev.markdown import markdown
from posts.models import Post, PostUpload


VALID_CONTENT_TEMPLATETAG_FILTERS = ["order_by", "tags"]


def generate_post_link_from_title(title: str) -> str:
    return slugify(title)


def strip_and_parse_tags(tags: str) -> list[str]:
    return [tag.strip() for tag in tags.split(",")]


def render_content_templatetag(context_key: str, template_name: str, queryset: QuerySet) -> str:
    return render_to_string(template_name=template_name, context={context_key: queryset})


def create_content_templatetag_filter_from_match(content_filter_match: str) -> Optional[Q]:
    try:
        key, value = content_filter_match.split(":")
    except ValueError:
        return None

    if key not in VALID_CONTENT_TEMPLATETAG_FILTERS:
        return None

    query = None

    match key:
        case "tags":
            values = [v.strip() for v in value.split(",")]
            query = Q(**{"tags__overlap": values})
        case _:
            query = None

    return query


# TODO (willmeyers): Ensure safe inserting of html from tags. Test XSS and other vulns
def render_post(post: Post) -> str:
    def replace_match_with_rendered_template(match):
        """
        Callback function used for sub'ing matches
        """
        match = match.group(0)
        kind = match.replace("{{", "").replace("}}", "").strip().split("|")[0]
        filters = match.replace("{{", "").replace("}}", "").strip().split("|")[1:]

        final_query = Q(user=post.user)
        order_by = False

        try:
            for f in filters:
                if f.startswith("order_by"):
                    order_by = f.split(":")[1]
                    continue
                query = create_content_templatetag_filter_from_match(content_filter_match=f)
                final_query &= query if query else final_query
        except IndexError as err:
            print(err)
            pass


        model = Post
        if kind == "post_uploads" or kind == "uploads":
            model = PostUpload

        content_queryset = model.objects.filter(final_query)
        if order_by:
            content_queryset = content_queryset.order_by(order_by)

        print(kind, content_queryset)

        return render_content_templatetag(
            context_key=kind,
            template_name=f"_partials/{kind}_list.html",
            queryset=content_queryset
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
