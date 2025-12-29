"""Posts service layer."""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.posts import models, schemas, exceptions
from src.posts.constants import POST_STATUS_PUBLISHED
from src.pagination import PaginationParams, PaginatedResponse


def get_post_by_id(db: Session, post_id: int) -> Optional[models.Post]:
    """Get post by ID."""
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_posts(
    db: Session,
    pagination: PaginationParams,
    author_id: Optional[int] = None,
    published_only: bool = False
) -> PaginatedResponse[schemas.PostListResponse]:
    """Get paginated list of posts."""
    query = db.query(models.Post)
    
    if author_id:
        query = query.filter(models.Post.author_id == author_id)
    
    if published_only:
        query = query.filter(
            models.Post.is_published == True,
            models.Post.status == POST_STATUS_PUBLISHED
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    posts = query.order_by(models.Post.created_at.desc()).offset(pagination.skip).limit(pagination.limit).all()
    
    return PaginatedResponse.create(
        items=[schemas.PostListResponse.model_validate(post) for post in posts],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size
    )


def create_post(db: Session, post: schemas.PostCreate, author_id: int) -> models.Post:
    """Create a new post."""
    db_post = models.Post(
        title=post.title,
        content=post.content,
        status=post.status,
        author_id=author_id,
        is_published=(post.status == POST_STATUS_PUBLISHED)
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(
    db: Session,
    post_id: int,
    post_update: schemas.PostUpdate,
    author_id: int,
    is_admin: bool = False
) -> models.Post:
    """Update a post."""
    db_post = get_post_by_id(db, post_id)
    if not db_post:
        raise exceptions.PostNotFoundError()
    
    # Check ownership
    if db_post.author_id != author_id and not is_admin:
        raise exceptions.UnauthorizedPostAccessError()
    
    # Update fields
    if post_update.title is not None:
        db_post.title = post_update.title
    if post_update.content is not None:
        db_post.content = post_update.content
    if post_update.status is not None:
        db_post.status = post_update.status
    if post_update.is_published is not None:
        db_post.is_published = post_update.is_published
    
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int, author_id: int, is_admin: bool = False) -> bool:
    """Delete a post."""
    db_post = get_post_by_id(db, post_id)
    if not db_post:
        raise exceptions.PostNotFoundError()
    
    # Check ownership
    if db_post.author_id != author_id and not is_admin:
        raise exceptions.UnauthorizedPostAccessError()
    
    db.delete(db_post)
    db.commit()
    return True

