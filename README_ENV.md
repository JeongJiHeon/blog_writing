# 환경 변수 설정 가이드

## 빠른 시작

### 1. .env 파일 생성

터미널에서 실행:

```bash
cd /Users/jeongjiheon/Documents/프로젝트/blog_writing
python3 scripts/setup_env.py
```

또는 직접 `.env` 파일을 생성하세요:

```bash
cp .env.example .env
```

그리고 `.env` 파일을 열어서 다음 정보를 입력하세요:

```env
# GitHub 설정
GITHUB_TOKEN=your-github-token-here
GITHUB_USERNAME=your-github-username
GITHUB_REPO=blog_writing

# 애플리케이션 설정
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-admin-password
DATABASE_URL=sqlite:///./blog.db
```

### 2. GitHub Token 생성

1. [GitHub Settings](https://github.com/settings/tokens) → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. **Generate new token** → **Generate new token (classic)** 클릭
3. 토큰 이름: `blog_writing_deploy`
4. 권한 선택:
   - ✅ `repo` (전체 권한)
   - ✅ `workflow` (선택사항)
5. **Generate token** 클릭
6. 생성된 토큰을 복사 (한 번만 보여줍니다!)

### 3. GitHub에 푸시

.env 파일 설정이 완료되면:

```bash
python3 scripts/github_push.py
```

또는:

```bash
./scripts/push.sh
```

## 환경 변수 설명

### GitHub 설정

- `GITHUB_TOKEN`: GitHub Personal Access Token
- `GITHUB_USERNAME`: GitHub 사용자명
- `GITHUB_REPO`: 저장소 이름 (기본: blog_writing)

### 애플리케이션 설정

- `SECRET_KEY`: JWT 토큰 암호화 키 (랜덤 문자열)
- `ADMIN_USERNAME`: 관리자 사용자명 (기본: admin)
- `ADMIN_PASSWORD`: 관리자 비밀번호
- `DATABASE_URL`: 데이터베이스 URL (기본: sqlite:///./blog.db)

## 보안 주의사항

⚠️ **중요**: 
- `.env` 파일은 절대 Git에 커밋하지 마세요!
- `.gitignore`에 이미 포함되어 있습니다
- GitHub Token을 공개하지 마세요
- 프로덕션에서는 더 강력한 비밀번호를 사용하세요

## 문제 해결

### GitHub 푸시 실패 시

1. **토큰 권한 확인**: `repo` 권한이 있는지 확인
2. **저장소 존재 확인**: GitHub에 저장소가 생성되어 있는지 확인
3. **토큰 만료 확인**: 토큰이 만료되지 않았는지 확인

### .env 파일이 인식되지 않을 때

```bash
# .env 파일 위치 확인
ls -la .env

# Python 스크립트에서 직접 확인
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GITHUB_TOKEN'))"
```

