from django.test import TestCase
from django.utils.text import slugify

from authusers.models import AuthUser


class GenerateAuthuserSlugTests(TestCase):
    def test_generate_unique_slug(self):
        # Test case when full names are the same
        user1 = AuthUser.objects.create_user(
            email="tombradyoffical@example.com",
            password="r3a11yS3cur3P@ssw0rD",
            full_name = "Tom Brady"
        )

        user2 = AuthUser.objects.create_user(
            email="tombradyregularguy@example.com",
            password="r3a11yS3cur3P@ssw0rD",
            full_name = "Tom Brady"
        )

        self.assertNotEqual(user1.slug, user2.slug)
        self.assertEqual(user1.slug, slugify(user1.full_name))
        self.assertEqual(user2.slug, slugify(user2.full_name)+"2")

        user1.delete()
        user2.delete()

        # Test case when email username and full_name are the same
        user1 = AuthUser.objects.create_user(
            email="tom@example.com",
            password="r3a11yS3cur3P@ssw0rD",
        )

        user2 = AuthUser.objects.create_user(
            email="tombradyregularguy@example.com",
            password="r3a11yS3cur3P@ssw0rD",
            full_name="Tom"
        )

        self.assertNotEqual(user1.slug, user2.slug)
        self.assertEqual(user1.slug, slugify(user1.email.split("@")[0]))
        self.assertEqual(user2.slug, slugify(user2.full_name)+"2")
