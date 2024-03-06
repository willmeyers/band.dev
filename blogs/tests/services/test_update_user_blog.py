from django.test import TestCase

from authusers.tests.factories import create_fake_user
from blogs.schemas import CreateBlogRequestBody, UpdateBlogRequestBody
from blogs.services import create_user_blog, update_user_blog


class UpdateBlogTests(TestCase):
    def setUp(self) -> None:
        self.user = create_fake_user()
        self.blog = self.user.blog

    def test_update_blog(self):
        update_blog_request_body = UpdateBlogRequestBody(
            navbar="[Home](/) [Posts](/posts) Page[/page]",
            content="---\ntitle: Hello World\nsubdomain: hello-world\ncustom_domain: example.com\nmeta_description: My blog\nmeta_image: https://example.com/image.jpeg\n---\n#Header\nHello world.",
        )

        blog = update_user_blog(blog=self.blog, request_body=update_blog_request_body)

        self.assertEqual(blog.title, "Hello World")

    def test_update_blog_with_empty_content(self):
        update_blog_request_body = UpdateBlogRequestBody(
            navbar="[Home](/) [Posts](/posts) Page[/page]", content=""
        )

        blog = update_user_blog(blog=self.blog, request_body=update_blog_request_body)

        self.assertEqual(blog.title, f"{blog.user.slug}'s Blog")
