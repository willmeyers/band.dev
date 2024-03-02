import re

from django import template

from band_dev.markdown import markdown


register = template.Library()


@register.filter(name="md2html")
def markdown_to_html(markdown_text: str) -> str:
    html = markdown.convert(markdown_text)

    return html


@register.filter(name="md2innerhtml")
def markdown_to_inner_html(markdown_text: str) -> str:
    html = markdown.convert(markdown_text)
    pattern = r'^<[^>]+>(.*)<\/[^>]+>$'
    html = re.sub(pattern, r'\1', html, flags=re.DOTALL)

    return html
