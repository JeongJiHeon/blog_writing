# 빠른 시작 - .env 설정 및 GitHub 푸시

## 1. .env 파일 생성

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
# GitHub 설정
GITHUB_TOKEN=여기에-토큰-입력
GITHUB_USERNAME=여기에-사용자명-입력
GITHUB_REPO=blog_writing

# 애플리케이션 설정
SECRET_KEY=GdllpTKGwxNfiK3sBzoc2J2SxdnN9imfNipNe3eJhZY
ADMIN_USERNAME=admin
ADMIN_PASSWORD=여기에-비밀번호-입력
DATABASE_URL=sqlite:///./blog.db
```

## 2. GitHub Token 생성 (아직 안 했다면)

1. [GitHub Settings](https://github.com/settings/tokens) → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. **Generate new token** → **Generate new token (classic)** 클릭
3. 토큰 이름: `blog_writing_deploy`
4. 권한: ✅ `repo` (전체 권한)
5. **Generate token** 클릭 후 토큰 복사

## 3. GitHub 저장소 생성

1. [GitHub](https://github.com) 로그인
2. **"+"** → **"New repository"** 클릭
3. 저장소 이름: `blog_writing` (또는 원하는 이름)
4. **"Create repository"** 클릭

## 4. 자동 푸시

.env 파일을 저장한 후:

```bash
python3 scripts/github_push.py
```

완료! 🎉

## 또는 인터랙티브 설정

```bash
python3 scripts/setup_env.py
```

이 명령어를 실행하면 단계별로 입력을 받습니다.

