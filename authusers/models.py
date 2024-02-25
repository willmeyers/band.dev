from django.apps import apps
from django.db import models
from django.db.models import Count, Max
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.text import slugify

from band_dev.models import BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extras):
        if not email:
            raise ValueError("missing required field: email")

        email = self.normalize_email(email)

        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )

        user = GlobalUserModel(email=email, **extras)
        user.password = make_password(password)
        user.slug = user.generate_slug()
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extras):
        extras.setdefault("is_staff", False)
        extras.setdefault("is_superuser", False)

        return self._create_user(email=email, password=password, **extras)


class AuthUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    full_name = models.TextField(null=True)
    slug = models.SlugField(unique=True)

    # Misc. user preferences
    allow_kudos = models.BooleanField(default=True)
    allow_subscriptions = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def generate_slug(self):
        slug_base = self.full_name if self.full_name else self.email.split("@")[0]
        base_slug = slugify(slug_base)

        similar_slug_count = AuthUser.objects.filter(slug__startswith=base_slug).count()

        if similar_slug_count < 1:
            return base_slug

        return f"{base_slug}{similar_slug_count + 1}"
