from typing import Optional, Any
from pydantic import BaseModel


class CreatePostRequestBody(BaseModel):
    content: str
    user_id: int
    blog_id: int


class UpdatePostRequestBody(BaseModel):
    content: str
    post_id: int


class AudioUploadRequestBody(BaseModel):
    user_id: int
    file_name: str
    content_type: str
    size: int
    file: Any


class PostMarkdownMetadata(BaseModel):
    title: str
    link: Optional[str]
    published_date: Optional[str]
    tags: Optional[str]
    class_name: Optional[str]
    meta_description: Optional[str]
    meta_image: Optional[str]
    is_discoverable: Optional[bool]
