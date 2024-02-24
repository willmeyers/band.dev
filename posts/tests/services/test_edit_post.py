from django.test import TestCase

from authusers.tests.factories import create_fake_user
from blogs.services import create_user_blog
from posts.schemas import CreatePostRequestBody, UpdatePostRequestBody
from posts.models import Post
from posts.services import create_post, update_post
from posts.utils import generate_post_link_from_title


class CreatePostTests(TestCase):
    def setUp(self) -> None:
        self.user = create_fake_user()
        self.blog = create_user_blog(user=self.user)
        self.post = create_post(
            request_body=CreatePostRequestBody(
                content="---\ntitle: Hello World\n---",
                user_id=self.user.id,
                blog_id=self.blog.id,
            ),
            request_files=[],
        )

    def test_update_post_without_files(self):
        update_post_request_body = UpdatePostRequestBody(
            post_id=self.post.id, content="---\ntitle: Hello World Updated\n---"
        )

        post = update_post(
            post=self.post, request_body=update_post_request_body, request_files=[]
        )

        expected_updated_content = "---\ntitle: Hello World Updated\nlink: hello-world-updated\n---"

        self.assertEqual(post.content, expected_updated_content)
        self.assertEqual(post.title, "Hello World Updated")
        self.assertEqual(post.link, generate_post_link_from_title(title=post.title))
        self.assertEqual(post.meta_image, None)
        self.assertEqual(post.meta_description, None)
        self.assertEqual(post.class_name, None)

        self.assertTrue(post.is_discoverable)
        self.assertFalse(post.is_page)

        self.assertEqual(post.user, self.user)
        self.assertEqual(post.blog, self.blog)
