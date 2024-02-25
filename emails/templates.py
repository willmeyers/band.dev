from typing_extensions import Optional
from django.conf import settings
from django.template import Template, Context
from django.template.loader import render_to_string

from band_dev.settings import SITE_URL_USE_SSL


class EmailTemplate:
    title: str
    body: str
    base_template_name: str = "emails/base_email.html"

    def __init__(self,
        title: str,
        body: str,
        base_template_name: Optional[str] = None
    ):
        self.title = title
        self.body = body

        if base_template_name:
            self.base_template_name = base_template_name

    def render_with_context(self, **context):
        body_template = Template(self.body)
        body_template_str = body_template.render(Context(context))


        template_str = render_to_string(
            self.base_template_name,
            context={
                "site_url": settings.SITE_URL,
                "title": self.title,
                "body": body_template_str,
                **context
            }
        )

        return template_str


activate_account_email_template = EmailTemplate(
    title="Verify your Email",
    body="Please click the link to activate your account so you can start uploading.\n\n[activate account]({{ site_url }}{% url 'authusers:activate_account' readable_user_id=readable_user_id token=token %})"
)
