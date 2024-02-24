from django.test import TestCase
from django.conf import settings

from authusers.tests.factories import create_fake_user
from blogs.services import create_user_blog

class CreateUserBlogTests(TestCase):
    def setUp(self) -> None:
        self.user = create_fake_user()

    def test_create_user_blog(self):
        blog = create_user_blog(user=self.user)

        self.assertTrue(blog.sites.filter(name__endswith="__internal").exists())

        blog_internal_domain = blog.sites.get(name__endswith="__internal")

        self.assertEqual(blog.title, f"{self.user.slug}'s Blog")
        self.assertEqual(blog_internal_domain.domain, f"{self.user.slug}.{settings.SITE_URL}")
        self.assertEqual(blog.content, f"---\ntitle: {blog.title}\nband_domain: {blog.domain}\n---")
