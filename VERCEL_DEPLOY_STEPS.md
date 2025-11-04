# Vercel 배포 단계별 가이드

지금 바로 따라하세요!

## 1단계: Git 저장소 초기화

터미널에서 실행:

```bash
cd /Users/jeongjiheon/Documents/프로젝트/blog_writing

# Git 초기화
git init

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit for Vercel deployment"
```

## 2단계: GitHub 저장소 생성

1. [GitHub](https://github.com) 로그인
2. 우측 상단 "+" → "New repository" 클릭
3. 저장소 이름: `blog_writing` (또는 원하는 이름)
4. Public 또는 Private 선택
5. **"Create repository"** 클릭 (README, .gitignore 등은 체크하지 마세요)

## 3단계: GitHub에 푸시

GitHub에서 생성된 저장소의 URL을 복사한 후:

```bash
# GitHub 저장소 연결 (URL을 실제 저장소 URL로 변경)
git remote add origin https://github.com/yourusername/blog_writing.git

# 브랜치 이름 변경
git branch -M main

# 푸시
git push -u origin main
```

## 4단계: Vercel 가입 및 배포

### 4-1. Vercel 가입

1. [Vercel](https://vercel.com) 접속
2. "Sign Up" 클릭
3. **"Continue with GitHub"** 선택
4. GitHub 권한 승인

### 4-2. 프로젝트 생성

1. "Add New..." → **"Project"** 클릭
2. GitHub 저장소 선택 (`blog_writing`)
3. 프로젝트 설정:
   - **Framework Preset**: `Other`
   - **Root Directory**: `./` (기본값)
   - **Build Command**: (비워두기)
   - **Output Directory**: (비워두기)
   - **Install Command**: `pip install -r requirements.txt`

### 4-3. 환경 변수 설정

"Environment Variables" 섹션에서 다음 변수 추가:

1. **시크릿 키 생성** (터미널에서):
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. Vercel에서 변수 추가:
   - `SECRET_KEY` = (생성한 시크릿 키)
   - `ADMIN_USERNAME` = `admin`
   - `ADMIN_PASSWORD` = (강력한 비밀번호 설정)
   - `DATABASE_URL` = `sqlite:///./blog.db`

### 4-4. 배포!

**"Deploy"** 버튼 클릭!

배포가 완료되면 (보통 1-2분):
- Vercel URL이 제공됩니다: `https://blog-writing-xxx.vercel.app`
- 브라우저에서 접속해서 확인하세요!

## 5단계: 도메인 연결

### 5-1. Vercel에서 도메인 추가

1. Vercel 프로젝트 → **"Settings"** 탭
2. **"Domains"** 메뉴 클릭
3. `mukbang.life` 입력
4. **"Add"** 클릭
5. DNS 레코드 확인 (나중에 필요)

### 5-2. Cloudflare 설정

#### Cloudflare 가입 (아직 안 했다면)

1. [Cloudflare](https://dash.cloudflare.com/sign-up) 가입
2. "Add a Site" 클릭
3. `mukbang.life` 입력
4. Free 플랜 선택
5. Continue

#### 네임서버 확인

Cloudflare가 네임서버를 제공합니다:
- 예: `violet.ns.cloudflare.com`, `walt.ns.cloudflare.com`

### 5-3. WordPress.com에서 네임서버 변경

1. [WordPress.com](https://wordpress.com) 로그인
2. **도메인** 메뉴 클릭
3. `mukbang.life` 선택
4. **도메인 설정** 또는 **고급 설정** 찾기
5. **네임서버 변경** 찾기
6. Cloudflare의 네임서버 2개 입력:
   ```
   violet.ns.cloudflare.com (예시)
   walt.ns.cloudflare.com (예시)
   ```
   (실제 네임서버는 Cloudflare에서 확인하세요)
7. 저장

### 5-4. DNS 레코드 추가

네임서버 전파 확인 (10분~2시간):
- https://www.whatsmydns.net/#NS/mukbang.life

전파 완료 후:

1. Cloudflare → **DNS** 메뉴
2. **"Add record"** 클릭

**CNAME 레코드 추가:**
- **Type**: `CNAME`
- **Name**: `@`
- **Target**: `cname.vercel-dns.com` (Vercel에서 안내한 주소)
- **Proxy status**: 🟠 **Proxied** (주황색 구름) ⭐
- **TTL**: Auto

**www 서브도메인:**
- **Type**: `CNAME`
- **Name**: `www`
- **Target**: `cname.vercel-dns.com`
- **Proxy status**: 🟠 **Proxied**
- **TTL**: Auto

### 5-5. 완료 확인

잠시 후 (몇 분~1시간):
- https://mukbang.life 접속 확인
- https://www.mukbang.life 접속 확인

## 문제 해결

### 배포 실패 시

1. Vercel → **Deployments** → 실패한 배포 클릭
2. 로그 확인
3. 일반적인 문제:
   - 환경 변수 누락 → Settings → Environment Variables 확인
   - requirements.txt 오류 → 로그 확인

### 도메인이 작동하지 않는 경우

1. DNS 전파 확인: https://www.whatsmydns.net/
2. Vercel에서 도메인 상태 확인
3. Cloudflare DNS 레코드 확인

### SQLite 데이터베이스 문제

Vercel 서버리스 환경에서는 SQLite가 제한적입니다.

**해결책:**
1. **임시**: 작동은 하지만 제한적
2. **권장**: Vercel Postgres 사용 (추가 설정 필요)
3. **또는**: Railway/Vercel KV 사용

## 다음 단계

✅ 배포 완료 후:
1. https://mukbang.life/docs 에서 API 문서 확인
2. 관리자 계정으로 로그인 테스트
3. 첫 게시글 작성
4. Google AdSense 설정

## 체크리스트

- [ ] Git 저장소 초기화
- [ ] GitHub 저장소 생성
- [ ] GitHub에 푸시
- [ ] Vercel 가입
- [ ] Vercel 프로젝트 생성
- [ ] 환경 변수 설정
- [ ] 배포 확인
- [ ] Cloudflare 설정
- [ ] 네임서버 변경
- [ ] DNS 레코드 추가
- [ ] 도메인 접속 확인

준비되셨나요? 위 단계를 순서대로 따라하세요! 🚀

