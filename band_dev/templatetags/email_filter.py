from django import template


register = template.Library()


@register.filter("nl2br")
def replace_newlines_with_br(text: str) -> str:
    return text.replace("\n", "<br>")
