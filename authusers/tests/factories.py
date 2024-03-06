import factory

from band_dev.tests.faker import faker
from authusers.models import AuthUser
from authusers.services import create_user, CreateUserRequestBody



def create_fake_user(**kwargs) -> AuthUser:
    pwd = faker.password()
    request_body = CreateUserRequestBody(
        email=faker.email(), full_name=faker.name(), password=pwd, confirm_password=pwd, **kwargs
    )

    user = create_user(request_body=request_body)

    return user
