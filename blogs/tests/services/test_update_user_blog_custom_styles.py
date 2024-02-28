from django.test import TestCase

from blogs.services import update_user_blog_custom_styles
from blogs.schemas import UpdateBlogCustomStylesRequestBody
from authusers.tests.factories import create_fake_user


class UpdateBlogCustomStylesTests(TestCase):
    def setUp(self) -> None:
        self.user = create_fake_user()
        self.blog = self.user.blog

    def test_update_user_blog_custom_styles(self):
        request_body = UpdateBlogCustomStylesRequestBody(
            custom_styles=":root { --background-color: red; }",
        )

    def test_update_user_blog_custom_music_player_styles(self):
        request_body = UpdateBlogCustomStylesRequestBody(
            custom_music_player_styles=":host { --background: white; }"
        )
