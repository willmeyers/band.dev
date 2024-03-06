from django.test import TestCase
from django.conf import settings

from authusers.tests.factories import create_fake_user
from blogs.services import create_user_blog


class CreateUserBlogTests(TestCase):
    def setUp(self) -> None:
        self.user = create_fake_user()
        self.blog = self.user.blog

    def test_create_user_blog(self):
        self.assertTrue(self.blog.sites.filter(name__endswith="__internal").exists())

        blog_internal_domain = self.blog.sites.get(name__endswith="__internal")

        self.assertEqual(self.blog.title, f"{self.user.slug}'s Blog")
        self.assertEqual(
            blog_internal_domain.domain, f"{self.user.slug}.{settings.SITE_DOMAIN}"
        )
        self.assertEqual(
            self.blog.content, f"---\ntitle: {self.blog.title}\nband_domain: {self.blog.domain}\n---"
        )
