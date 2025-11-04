"""
게시글(Posts) CRUD API 라우터
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Post, User
from schemas import PostCreate, PostUpdate, PostResponse, PostListResponse
from auth import get_current_user, get_current_admin_user
from datetime import datetime
import re

router = APIRouter(prefix="/api/posts", tags=["posts"])


def create_slug(title: str) -> str:
    """제목으로부터 슬러그 생성"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')


def ensure_unique_slug(db: Session, slug: str, exclude_id: Optional[int] = None) -> str:
    """고유한 슬러그 생성"""
    original_slug = slug
    counter = 1
    while True:
        query = db.query(Post).filter(Post.slug == slug)
        if exclude_id:
            query = query.filter(Post.id != exclude_id)
        if not query.first():
            return slug
        slug = f"{original_slug}-{counter}"
        counter += 1


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """게시글 생성"""
    slug = ensure_unique_slug(db, create_slug(post.title))
    
    db_post = Post(
        title=post.title,
        slug=slug,
        content=post.content,
        excerpt=post.excerpt,
        author_id=current_user.id,
        is_published=post.is_published
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/", response_model=List[PostListResponse])
def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    published_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """게시글 목록 조회"""
    query = db.query(Post)
    
    if published_only:
        query = query.filter(Post.is_published == True)
    
    query = query.order_by(Post.created_at.desc())
    posts = query.offset(skip).limit(limit).all()
    return posts


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """게시글 상세 조회"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    
    # 조회수 증가 (발행된 게시글만)
    if post.is_published:
        post.view_count += 1
        db.commit()
    
    return post


@router.get("/slug/{slug}", response_model=PostResponse)
def get_post_by_slug(slug: str, db: Session = Depends(get_db)):
    """슬러그로 게시글 조회"""
    post = db.query(Post).filter(Post.slug == slug).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    
    # 조회수 증가 (발행된 게시글만)
    if post.is_published:
        post.view_count += 1
        db.commit()
    
    return post


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """게시글 수정"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    
    # 작성자 또는 관리자만 수정 가능
    if post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="게시글을 수정할 권한이 없습니다"
        )
    
    # 제목이 변경되면 슬러그도 변경
    if post_update.title and post_update.title != post.title:
        post.slug = ensure_unique_slug(db, create_slug(post_update.title), exclude_id=post_id)
    
    update_data = post_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)
    
    post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """게시글 삭제"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    
    # 작성자 또는 관리자만 삭제 가능
    if post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="게시글을 삭제할 권한이 없습니다"
        )
    
    db.delete(post)
    db.commit()
    return None

