from django.test import TestCase

from authusers.tests.factories import AuthUserFactory
from blogs.services import create_user_blog
from posts.schemas import CreatePostRequestBody
from posts.models import Post
from posts.services import create_post
from posts.utils import generate_post_link_from_title


class CreatePostTests(TestCase):
    def setUp(self) -> None:
        self.user = AuthUserFactory()
        self.blog = create_user_blog(user=self.user)

    def test_create_post_without_files(self):
        create_post_request_body = CreatePostRequestBody(
            user_id=self.user.id,
            blog_id=self.blog.id,
            content="---\ntitle: Hello World\n---\n# Hello World"
        )

        post = create_post(request_body=create_post_request_body, request_files=[])

        self.assertEqual(post.content, create_post_request_body.content)
        self.assertEqual(post.title, "Hello World")
        self.assertEqual(post.link, generate_post_link_from_title(title=post.title))
        self.assertEqual(post.meta_image, None)
        self.assertEqual(post.meta_description, None)
        self.assertEqual(post.class_name, None)

        self.assertTrue(post.is_discoverable)
        self.assertFalse(post.is_page)

        self.assertEqual(post.user, self.user)
        self.assertEqual(post.blog, self.blog)
