from django.conf import settings
from django.core.mail import send_mail

from authusers.models import AuthUser
from authusers.utils import account_activation_token
from emails.templates import activate_account_email_template


def send_account_activation_email_to_user(user: AuthUser):
    token = account_activation_token.make_token(user=user)

    message = activate_account_email_template.render_with_context(
        readable_user_id=user.readable_id,
        token=token
    )

    send_mail(
        subject=activate_account_email_template.title,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )
