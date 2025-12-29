"""Posts utility functions."""
from typing import Optional
from src.posts.models import Post
from src.posts.constants import POST_STATUS_PUBLISHED


def is_post_published(post: Post) -> bool:
    """Check if post is published."""
    return post.is_published and post.status == POST_STATUS_PUBLISHED


def can_user_access_post(post: Post, user_id: int, is_admin: bool = False) -> bool:
    """Check if user can access post."""
    if is_admin:
        return True
    if is_post_published(post):
        return True
    return post.author_id == user_id


def sanitize_post_content(content: str) -> str:
    """Sanitize post content (basic implementation)."""
    # In production, use a proper HTML sanitizer like bleach
    return content.strip()


def generate_post_slug(title: str) -> str:
    """Generate a URL-friendly slug from post title."""
    import re
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

