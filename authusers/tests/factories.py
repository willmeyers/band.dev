import factory

from band_dev.tests.faker import faker
from authusers.models import AuthUser
from blogs.tests.factories import BlogFactory


def create_fake_user(**kwargs):
    user = AuthUser.objects.create_user(
        email=faker.email(), full_name=faker.name(), password=faker.password(), **kwargs
    )

    return user
