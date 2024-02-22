import factory

from band_dev.tests.faker import faker
from authusers.models import AuthUser
from blogs.tests.factories import BlogFactory


class AuthUserFactory(factory.django.DjangoModelFactory):
    email = factory.LazyAttribute(lambda _: faker.email())
    full_name = factory.LazyAttribute(lambda _: faker.name())
    slug = factory.LazyAttribute(lambda obj: AuthUser().generate_slug())

    class Meta:
        model = AuthUser
