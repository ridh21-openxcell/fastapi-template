"""Posts database models."""
from sqlalchemy import Column, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.models import BaseModel
from src.posts.constants import POST_STATUS_DRAFT


class Post(BaseModel):
    """Post model."""
    __tablename__ = "posts"
    
    title = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    status = Column(String, default=POST_STATUS_DRAFT, nullable=False)
    is_published = Column(Boolean, default=False)
    author_id = Column(ForeignKey("users.id"), nullable=False)
    
    # Relationship
    author = relationship("User", backref="posts")
    
    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title}, author_id={self.author_id})>"

