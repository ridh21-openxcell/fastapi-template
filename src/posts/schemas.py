"""Posts Pydantic schemas."""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from src.posts.constants import POST_STATUS_DRAFT, POST_STATUS_PUBLISHED, POST_STATUS_ARCHIVED


class PostBase(BaseModel):
    """Base post schema."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    status: str = Field(default=POST_STATUS_DRAFT)


class PostCreate(PostBase):
    """Post creation schema."""
    pass


class PostUpdate(BaseModel):
    """Post update schema."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    status: Optional[str] = None
    is_published: Optional[bool] = None


class PostResponse(PostBase):
    """Post response schema."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_published: bool
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class PostListResponse(BaseModel):
    """Post list response schema."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    status: str
    is_published: bool
    author_id: int
    created_at: datetime

