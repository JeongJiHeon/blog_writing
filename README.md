# 블로그 시스템

FastAPI 기반의 블로그 관리 시스템입니다. 게시글, 댓글, 사용자 관리 등의 CRUD 기능을 제공합니다.

## 주요 기능

- ✅ **게시글(Posts) CRUD**: 게시글 생성, 조회, 수정, 삭제
- ✅ **댓글(Comments) CRUD**: 댓글 작성, 조회, 수정, 삭제, 승인
- ✅ **사용자 인증**: 회원가입, 로그인, JWT 토큰 기반 인증
- ✅ **미디어 관리**: 이미지 및 파일 업로드
- ✅ **관리자 기능**: 관리자 권한 관리
- ✅ **RESTful API**: 표준 REST API 제공

## 설치

1. 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 환경 변수 설정 (선택사항):
```bash
cp .env.example .env
# .env 파일을 열어서 설정 수정
```

## 실행

```bash
python run.py
```

또는

```bash
uvicorn main:app --reload
```

서버가 실행되면 다음 주소에서 접근할 수 있습니다:
- API 서버: http://localhost:8000
- API 문서: http://localhost:8000/docs
- 대체 문서: http://localhost:8000/redoc

## 기본 관리자 계정

- 사용자명: `admin`
- 비밀번호: `admin123`

(환경 변수에서 변경 가능)

## API 엔드포인트

### 인증 (`/api/auth`)
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `GET /api/auth/me` - 현재 사용자 정보

### 게시글 (`/api/posts`)
- `GET /api/posts/` - 게시글 목록 조회
- `GET /api/posts/{post_id}` - 게시글 상세 조회
- `GET /api/posts/slug/{slug}` - 슬러그로 게시글 조회
- `POST /api/posts/` - 게시글 생성 (인증 필요)
- `PUT /api/posts/{post_id}` - 게시글 수정 (인증 필요)
- `DELETE /api/posts/{post_id}` - 게시글 삭제 (인증 필요)

### 댓글 (`/api/comments`)
- `GET /api/comments/posts/{post_id}` - 게시글의 댓글 목록
- `POST /api/comments/posts/{post_id}` - 댓글 작성
- `PUT /api/comments/{comment_id}` - 댓글 수정 (인증 필요)
- `DELETE /api/comments/{comment_id}` - 댓글 삭제 (인증 필요)
- `POST /api/comments/{comment_id}/approve` - 댓글 승인 (관리자만)

### 미디어 (`/api/media`)
- `POST /api/media/upload` - 파일 업로드 (인증 필요)
- `GET /api/media/files/{filename}` - 파일 조회

## 사용 예제

### 1. 회원가입
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. 로그인
```bash
curl -X POST "http://localhost:8000/api/auth/login?username=admin&password=admin123"
```

### 3. 게시글 생성
```bash
curl -X POST "http://localhost:8000/api/posts/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "첫 번째 게시글",
    "content": "<p>게시글 내용입니다.</p>",
    "excerpt": "게시글 요약",
    "is_published": true
  }'
```

### 4. 게시글 목록 조회
```bash
curl "http://localhost:8000/api/posts/?published_only=true&limit=10"
```

### 5. 파일 업로드
```bash
curl -X POST "http://localhost:8000/api/media/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/image.jpg"
```

## 프로젝트 구조

```
blog_writing/
├── main.py              # FastAPI 메인 애플리케이션
├── run.py               # 서버 실행 스크립트
├── config.py            # 설정 관리
├── database.py          # 데이터베이스 설정
├── models.py            # 데이터베이스 모델
├── schemas.py           # Pydantic 스키마
├── auth.py              # 인증 유틸리티
├── routers/             # API 라우터
│   ├── posts.py         # 게시글 API
│   ├── comments.py      # 댓글 API
│   ├── auth.py          # 인증 API
│   └── media.py         # 미디어 API
├── templates/           # HTML 템플릿
├── uploads/             # 업로드된 파일 (자동 생성)
├── requirements.txt     # 패키지 의존성
└── README.md           # 문서
```

## 데이터베이스

기본적으로 SQLite를 사용합니다. 다른 데이터베이스를 사용하려면 `config.py` 또는 환경 변수에서 `DATABASE_URL`을 변경하세요.

예:
- PostgreSQL: `postgresql://user:password@localhost/dbname`
- MySQL: `mysql://user:password@localhost/dbname`

## 배포 및 DNS 설정

### 🚀 배포 가이드
- **[Vercel 배포 단계별 가이드](VERCEL_DEPLOY_STEPS.md)** - Vercel 배포 완전 가이드 ⭐ **추천!**
- **[Vercel 도메인 오류 해결](VERCEL_DOMAIN_FIX.md)** - Invalid Configuration 오류 해결 ⚠️ **문제 해결!**
- **[Cloudflare 설정 가이드](CLOUDFLARE_SETUP.md)** - Cloudflare DNS 설정 완전 가이드 ⭐ **필수!**
- **[WordPress 도메인 사용 가이드](WORDPRESS_DOMAIN_GUIDE.md)** - WordPress에서 구매한 도메인 사용하기

프로덕션 환경에서는 다음 사항을 변경하세요:

1. `.env` 파일에서 `SECRET_KEY` 변경
2. 관리자 계정 비밀번호 변경
3. CORS 설정에서 허용된 도메인 지정
4. HTTPS 사용
5. 데이터베이스 백업 설정

## 라이선스

이 프로젝트는 자유롭게 사용 가능합니다.

