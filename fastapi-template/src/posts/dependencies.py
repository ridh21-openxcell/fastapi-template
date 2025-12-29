"""Posts dependencies."""
from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.posts import models, exceptions
from src.auth.dependencies import get_current_active_user
from src.auth import schemas as auth_schemas


def get_post_or_404(
    post_id: int,
    db: Session = Depends(get_db)
) -> models.Post:
    """Get post by ID or raise 404."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise exceptions.PostNotFoundError()
    return post


def verify_post_owner(
    post: models.Post = Depends(get_post_or_404),
    current_user: auth_schemas.UserResponse = Depends(get_current_active_user)
) -> models.Post:
    """Verify that the current user owns the post."""
    if post.author_id != current_user.id and not current_user.is_superuser:
        raise exceptions.UnauthorizedPostAccessError()
    return post

