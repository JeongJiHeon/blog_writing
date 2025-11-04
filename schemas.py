"""
Pydantic 스키마 (요청/응답 모델)
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# 사용자 스키마
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# 게시글 스키마
class PostBase(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    is_published: bool = False


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    is_published: Optional[bool] = None


class PostResponse(PostBase):
    id: int
    slug: str
    author_id: int
    view_count: int
    created_at: datetime
    updated_at: datetime
    author: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: Optional[str]
    author_id: int
    is_published: bool
    view_count: int
    created_at: datetime
    author: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True


# 댓글 스키마
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    author_name: Optional[str] = None
    author_email: Optional[EmailStr] = None


class CommentResponse(CommentBase):
    id: int
    post_id: int
    author_id: Optional[int]
    author_name: Optional[str]
    author_email: Optional[str]
    is_approved: bool
    created_at: datetime
    author: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True


# 인증 스키마
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

