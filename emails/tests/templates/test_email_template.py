from django.test import TestCase

from emails.templates import EmailTemplate


class EmailTemplateTests(TestCase):
    def test_email_template_render_with_context(self):
        email_template = EmailTemplate(
            title="Test Email",
            body="This is a test body. It should end with: **{{ test_variable }}**",
        )

        rendered_template = email_template.render_with_context(test_variable=42)

        self.assertTrue("**{{ test_variable }}**" not in rendered_template)
