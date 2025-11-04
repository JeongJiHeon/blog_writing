"""
FastAPI 메인 애플리케이션
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import posts, comments, auth, media
from config import settings
import os

# FastAPI 앱 생성
app = FastAPI(
    title="Blog API",
    description="블로그 관리 시스템 API",
    version="1.0.0"
)

# CORS 설정
# 프로덕션에서는 특정 도메인만 허용하도록 환경 변수로 설정 가능
# 예: CORS_ORIGINS=https://mukbang.life,https://www.mukbang.life
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(auth.router)
app.include_router(media.router)

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 정적 파일 서빙 (Vercel 서버리스 환경에서는 제한적)
# Vercel에서는 /uploads 경로를 별도로 처리하거나 외부 저장소(S3, Cloudinary) 사용 권장
if not os.environ.get("VERCEL") and os.path.exists(settings.upload_dir):
    from fastapi.staticfiles import StaticFiles
    app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")


# Vercel 서버리스 환경에서는 startup 이벤트가 매 요청마다 실행되지 않을 수 있음
# 대신 lazy initialization 사용
_initialized = False

def ensure_initialized():
    """데이터베이스 및 관리자 계정 초기화 (lazy)"""
    global _initialized
    if _initialized:
        return
    
    try:
        # 데이터베이스 초기화
        init_db()
        # 관리자 계정 생성
        from database import SessionLocal
        from models import User
        from auth import get_password_hash
        
        db = SessionLocal()
        try:
            admin = db.query(User).filter(User.username == settings.admin_username).first()
            if not admin:
                admin = User(
                    username=settings.admin_username,
                    email=f"{settings.admin_username}@example.com",
                    hashed_password=get_password_hash(settings.admin_password),
                    is_admin=True
                )
                db.add(admin)
                db.commit()
                print(f"관리자 계정 생성 완료: {settings.admin_username}")
        finally:
            db.close()
        
        _initialized = True
    except Exception as e:
        print(f"초기화 오류 (무시 가능): {e}")


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    ensure_initialized()


@app.middleware("http")
async def init_middleware(request: Request, call_next):
    """요청마다 초기화 확인 (서버리스 환경 대응)"""
    ensure_initialized()
    response = await call_next(request)
    return response


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """루트 경로 - 블로그 메인 페이지"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "ok"}

