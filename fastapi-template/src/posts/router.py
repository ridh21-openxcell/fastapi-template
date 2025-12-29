"""Posts router endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.posts import schemas, service, dependencies, models
from src.auth.dependencies import get_current_active_user
from src.auth import schemas as auth_schemas
from src.pagination import PaginationParams, PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[schemas.PostListResponse])
async def list_posts(
    pagination: PaginationParams = Depends(),
    published_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get list of posts."""
    return service.get_posts(db, pagination, published_only=published_only)


@router.get("/me", response_model=PaginatedResponse[schemas.PostListResponse])
async def list_my_posts(
    pagination: PaginationParams = Depends(),
    current_user: auth_schemas.UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's posts."""
    return service.get_posts(db, pagination, author_id=current_user.id, published_only=False)


@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: schemas.PostCreate,
    current_user: auth_schemas.UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new post."""
    return service.create_post(db, post, current_user.id)


@router.get("/{post_id}", response_model=schemas.PostResponse)
async def get_post(
    post: models.Post = Depends(dependencies.get_post_or_404)
):
    """Get a post by ID."""
    return schemas.PostResponse.model_validate(post)


@router.put("/{post_id}", response_model=schemas.PostResponse)
async def update_post(
    post_update: schemas.PostUpdate,
    post: models.Post = Depends(dependencies.verify_post_owner),
    current_user: auth_schemas.UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a post."""
    return service.update_post(db, post.id, post_update, current_user.id, current_user.is_superuser)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: models.Post = Depends(dependencies.verify_post_owner),
    current_user: auth_schemas.UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a post."""
    service.delete_post(db, post.id, current_user.id, current_user.is_superuser)
    return None

