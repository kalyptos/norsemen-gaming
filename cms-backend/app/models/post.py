"""Post data models"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PostCreate(BaseModel):
    """Model for creating a new blog post"""
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(default="Norsemen")
    game: str = Field(..., description="Game category")
    categories: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    featured: Optional[str] = Field(None, description="Featured image filename")
    description: str = Field(..., min_length=10, description="SEO description")
    content: str = Field(..., min_length=50, description="Markdown content")
    draft: bool = Field(default=True)


class PostUpdate(BaseModel):
    """Model for updating an existing post"""
    title: Optional[str] = None
    author: Optional[str] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    featured: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    draft: Optional[bool] = None


class Post(BaseModel):
    """Full post model with metadata"""
    slug: str
    title: str
    date: datetime
    author: str
    game: str
    categories: List[str]
    tags: List[str]
    featured: Optional[str]
    description: str
    content: str
    draft: bool
    file_path: str


class PostList(BaseModel):
    """List of posts with metadata"""
    posts: List[Post]
    total: int
    page: int
    per_page: int
