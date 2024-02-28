from typing import Optional
from pydantic import BaseModel


class CreateBlogRequestBody(BaseModel):
    user_id: int
    name: str


class BlogMarkdownMetadata(BaseModel):
    title: str
    band_domain: Optional[str] = None
    custom_domain: Optional[str] = None
    meta_description: Optional[str] = None
    meta_image: Optional[str] = None
    lang: Optional[str] = "en"


class UpdateBlogRequestBody(BaseModel):
    content: str
    navbar: Optional[str]


class UpdateBlogCustomStylesRequestBody(BaseModel):
    reset_to_default: Optional[bool] = False
    custom_styles: Optional[str] = None
    custom_music_player_styles: Optional[str] = None
