from django.db import transaction
from django.contrib.auth import authenticate

from band_dev.utils import decode_readable_id
from authusers.models import AuthUser
from authusers.utils import account_activation_token
from authusers.schemas import (
    CreateUserRequestBody,
    AuthenticateUserRequestBody,
    SettingsRequestBody,
)
from blogs.services import create_user_blog
from emails.services import send_account_activation_email_to_user


@transaction.atomic()
def create_user(request_body: CreateUserRequestBody) -> AuthUser:
    user = AuthUser.objects.create_user(
        email=request_body.email,
        full_name=request_body.full_name,
        password=request_body.password,
    )

    user.slug = user.generate_slug()
    create_user_blog(user=user)

    user.save()

    return user


def authenticate_user(request_body: AuthenticateUserRequestBody) -> AuthUser | None:
    user = authenticate(email=request_body.email, password=request_body.password)

    return user


def get_user_by_id(readable_id: str) -> AuthUser | None:
    valid, user_id = decode_readable_id(readable_id=readable_id)

    user = AuthUser.objects.filter(id=user_id).first()

    return user


@transaction.atomic
def activate_user_account(readable_id: str, token: str) -> bool:
    user = get_user_by_id(readable_id=readable_id)
    valid_token = account_activation_token.check_token(user=user, token=token)

    print(user, user.is_verified, token)

    if valid_token:
        user.is_verified = True
        user.save()

    return valid_token


def update_user_settings(user: AuthUser, request_body: SettingsRequestBody) -> AuthUser:
    if request_body.email:
        user.email = request_body.email

    if request_body.full_name:
        user.full_name = request_body.full_name

    user.allow_kudos = request_body.allow_kudos
    user.allow_subscriptions = request_body.allow_subscriptions

    user.save()

    return user
