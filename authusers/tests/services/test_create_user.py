from unittest.mock import patch
from django.test import TestCase
from authusers.models import AuthUser

from authusers.schemas import CreateUserRequestBody, AuthenticateUserRequestBody
from authusers.services import create_user, authenticate_user


class CreateUserTests(TestCase):
    def test_create_user(self):
        create_user_request = CreateUserRequestBody(
            email="user@example.com",
            password="r3a11yS3cur3P@ssw0rD",
            confirm_password="r3a11yS3cur3P@ssw0rD",
        )

        user = create_user(request_body=create_user_request)

        self.assertTrue(user.blog is not None)

    def test_authenticate_user_success(self):
        created_user = AuthUser.objects.create_user(
            email="user@example.com",
            password="r3a11yS3cur3P@ssw0rD",
        )

        auth_request_body = AuthenticateUserRequestBody(
            email="user@example.com",
            password="r3a11yS3cur3P@ssw0rD",
        )

        user = authenticate_user(request_body=auth_request_body)

        self.assertEqual(user, created_user)

    def test_authenticate_user_failure(self):
        auth_request_body = AuthenticateUserRequestBody(
            email="user@example.com",
            password="r3a11yS3cur3P@ssw0rD",
        )

        user = authenticate_user(request_body=auth_request_body)

        self.assertEqual(user, None)
