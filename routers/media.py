"""
미디어 업로드 API 라우터
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import aiofiles
from pathlib import Path
from database import get_db
from auth import get_current_user
from config import settings

router = APIRouter(prefix="/api/media", tags=["media"])

# 업로드 디렉토리 생성
upload_path = Path(settings.upload_dir)
upload_path.mkdir(exist_ok=True)


ALLOWED_EXTENSIONS = {
    'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp',
    'application/pdf'
}


def is_allowed_file(content_type: str) -> bool:
    """허용된 파일 타입인지 확인"""
    return content_type in ALLOWED_EXTENSIONS


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """파일 업로드"""
    # 파일 타입 확인
    if not is_allowed_file(file.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"허용되지 않은 파일 타입입니다. 허용된 타입: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 파일 크기 확인
    contents = await file.read()
    if len(contents) > settings.max_upload_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"파일 크기가 너무 큽니다. 최대 크기: {settings.max_upload_size / 1024 / 1024}MB"
        )
    
    # 파일 저장
    file_extension = Path(file.filename).suffix
    file_path = upload_path / f"{current_user.id}_{file.filename}"
    
    # 중복 파일명 처리
    counter = 1
    while file_path.exists():
        file_path = upload_path / f"{current_user.id}_{Path(file.filename).stem}_{counter}{file_extension}"
        counter += 1
    
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(contents)
    
    # URL 반환
    file_url = f"/api/media/files/{file_path.name}"
    return {
        "filename": file_path.name,
        "url": file_url,
        "size": len(contents),
        "content_type": file.content_type
    }


@router.get("/files/{filename}")
async def get_file(filename: str):
    """업로드된 파일 조회"""
    file_path = upload_path / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="파일을 찾을 수 없습니다"
        )
    
    return FileResponse(file_path)

