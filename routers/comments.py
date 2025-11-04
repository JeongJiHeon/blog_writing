"""
댓글(Comments) CRUD API 라우터
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Comment, Post, User
from schemas import CommentCreate, CommentResponse
from auth import get_current_user, get_current_admin_user
from fastapi.security import HTTPBearer

router = APIRouter(prefix="/api/comments", tags=["comments"])
security = HTTPBearer(auto_error=False)


def get_current_user_optional(
    credentials = Security(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """선택적 사용자 인증 (댓글 작성용)"""
    if not credentials:
        return None
    try:
        from jose import jwt
        from config import settings
        token = credentials.credentials
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username:
            user = db.query(User).filter(User.username == username).first()
            return user
    except Exception:
        pass
    return None


@router.post("/posts/{post_id}", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """댓글 생성 (비회원도 가능)"""
    # 게시글 존재 확인
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    
    # 게시글이 발행되지 않았으면 댓글 불가
    if not post.is_published:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="발행되지 않은 게시글에는 댓글을 작성할 수 없습니다"
        )
    
    db_comment = Comment(
        content=comment.content,
        post_id=post_id,
        author_id=current_user.id if current_user else None,
        author_name=comment.author_name if not current_user else None,
        author_email=comment.author_email if not current_user else None,
        is_approved=current_user is not None  # 회원은 자동 승인, 비회원은 승인 필요
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.get("/posts/{post_id}", response_model=List[CommentResponse])
def get_comments(
    post_id: int,
    approved_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """게시글의 댓글 목록 조회"""
    query = db.query(Comment).filter(Comment.post_id == post_id)
    
    if approved_only:
        query = query.filter(Comment.is_approved == True)
    
    comments = query.order_by(Comment.created_at.asc()).all()
    return comments


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """댓글 조회"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다"
        )
    return comment


@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment_update: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """댓글 수정"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다"
        )
    
    # 작성자 또는 관리자만 수정 가능
    if comment.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="댓글을 수정할 권한이 없습니다"
        )
    
    comment.content = comment_update.content
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """댓글 삭제"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다"
        )
    
    # 작성자 또는 관리자만 삭제 가능
    if comment.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="댓글을 삭제할 권한이 없습니다"
        )
    
    db.delete(comment)
    db.commit()
    return None


@router.post("/{comment_id}/approve", response_model=CommentResponse)
def approve_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """댓글 승인 (관리자만)"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다"
        )
    
    comment.is_approved = True
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/", response_model=List[CommentResponse])
def get_all_comments(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    approved_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """모든 댓글 목록 조회 (관리자만)"""
    query = db.query(Comment)
    
    if approved_only:
        query = query.filter(Comment.is_approved == True)
    
    comments = query.order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()
    return comments

