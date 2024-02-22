from django import template

from band_dev.markdown import markdown


register = template.Library()

@register.filter(name='md2html')
def markdown_to_html(markdown_text: str) -> str:
    html = markdown.convert(markdown_text)

    return html
