# 다음 단계 - 지금 바로 시작하세요! 🚀

## 전체 과정 요약 (5단계)

1. ✅ Git 저장소 초기화 및 커밋
2. ✅ GitHub 저장소 생성 및 푸시
3. ✅ Vercel 가입 및 배포
4. ✅ 환경 변수 설정
5. ✅ 도메인 연결 (mukbang.life)

---

## 1단계: Git 저장소 초기화 (지금 바로!)

터미널에서 실행:

```bash
cd /Users/jeongjiheon/Documents/프로젝트/blog_writing

# Git 초기화
git init

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: Blog system with Vercel deployment"
```

---

## 2단계: GitHub 저장소 생성 및 푸시

### 2-1. GitHub 저장소 생성

1. [GitHub](https://github.com) 로그인
2. 우측 상단 **"+"** → **"New repository"** 클릭
3. 저장소 이름: `blog_writing` (또는 원하는 이름)
4. **Public** 또는 **Private** 선택
5. ⚠️ **중요**: README, .gitignore, license는 체크하지 마세요!
6. **"Create repository"** 클릭

### 2-2. GitHub에 푸시

GitHub에서 생성된 저장소의 URL을 복사한 후:

```bash
# GitHub 저장소 연결 (URL을 실제 저장소 URL로 변경)
git remote add origin https://github.com/yourusername/blog_writing.git

# 브랜치 이름 변경
git branch -M main

# 푸시
git push -u origin main
```

⚠️ **GitHub 저장소 URL 예시**: `https://github.com/yourusername/blog_writing.git`

---

## 3단계: Vercel 가입 및 배포

### 3-1. Vercel 가입

1. [Vercel](https://vercel.com) 접속
2. **"Sign Up"** 클릭
3. **"Continue with GitHub"** 선택
4. GitHub 권한 승인

### 3-2. 프로젝트 생성

1. **"Add New..."** → **"Project"** 클릭
2. GitHub 저장소 선택 (`blog_writing`)
3. 프로젝트 설정:
   - **Framework Preset**: `Other`
   - **Root Directory**: `./` (기본값)
   - **Build Command**: (비워두기)
   - **Output Directory**: (비워두기)
   - **Install Command**: `pip install -r requirements.txt`

### 3-3. 환경 변수 설정 (중요!)

**시크릿 키 생성** (터미널에서):
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

생성된 시크릿 키를 복사한 후, Vercel에서 **"Environment Variables"** 섹션에 다음 변수 추가:

```
SECRET_KEY = (생성한 시크릿 키 붙여넣기)
ADMIN_USERNAME = admin
ADMIN_PASSWORD = (강력한 비밀번호 설정)
DATABASE_URL = sqlite:///./blog.db
```

### 3-4. 배포!

**"Deploy"** 버튼 클릭!

배포가 완료되면 (보통 1-2분):
- Vercel URL이 제공됩니다: `https://blog-writing-xxx.vercel.app`
- 브라우저에서 접속해서 확인하세요!

---

## 4단계: 도메인 연결 (mukbang.life)

### 4-1. Vercel에서 도메인 추가

1. Vercel 프로젝트 → **"Settings"** 탭
2. **"Domains"** 메뉴 클릭
3. `mukbang.life` 입력
4. **"Add"** 클릭
5. DNS 레코드 확인 (나중에 필요)

### 4-2. Cloudflare 설정

#### Cloudflare 가입 (아직 안 했다면)

1. [Cloudflare](https://dash.cloudflare.com/sign-up) 가입
2. **"Add a Site"** 클릭
3. `mukbang.life` 입력
4. **Free** 플랜 선택
5. Continue

#### 네임서버 확인

Cloudflare가 네임서버를 제공합니다:
- 예: `violet.ns.cloudflare.com`, `walt.ns.cloudflare.com`

### 4-3. WordPress.com에서 네임서버 변경

1. [WordPress.com](https://wordpress.com) 로그인
2. **도메인** 메뉴 클릭
3. `mukbang.life` 선택
4. **도메인 설정** 또는 **고급 설정** 찾기
5. **네임서버 변경** 찾기
6. Cloudflare의 네임서버 2개 입력
7. 저장

### 4-4. DNS 레코드 추가

네임서버 전파 확인 (10분~2시간):
- https://www.whatsmydns.net/#NS/mukbang.life

전파 완료 후:

1. Cloudflare → **DNS** 메뉴
2. **"Add record"** 클릭

**CNAME 레코드 추가:**
- **Type**: `CNAME`
- **Name**: `@`
- **Target**: `cname.vercel-dns.com` (Vercel에서 안내한 주소)
- **Proxy status**: 🟠 **Proxied** (주황색 구름)
- **TTL**: Auto

**www 서브도메인:**
- **Type**: `CNAME`
- **Name**: `www`
- **Target**: `cname.vercel-dns.com`
- **Proxy status**: 🟠 **Proxied**
- **TTL**: Auto

### 4-5. 완료 확인

잠시 후 (몇 분~1시간):
- https://mukbang.life 접속 확인
- https://www.mukbang.life 접속 확인

---

## 체크리스트

- [ ] Git 저장소 초기화
- [ ] 첫 커밋 완료
- [ ] GitHub 저장소 생성
- [ ] GitHub에 푸시
- [ ] Vercel 가입
- [ ] Vercel 프로젝트 생성
- [ ] 환경 변수 설정
- [ ] 배포 확인
- [ ] Cloudflare 설정
- [ ] WordPress.com에서 네임서버 변경
- [ ] DNS 레코드 추가
- [ ] 도메인 접속 확인

---

## 문제 해결

### Git 푸시 실패 시

```bash
# 원격 저장소 확인
git remote -v

# 원격 저장소 재설정
git remote remove origin
git remote add origin https://github.com/yourusername/blog_writing.git
```

### Vercel 배포 실패 시

1. Vercel → **Deployments** → 실패한 배포 클릭
2. 로그 확인
3. 일반적인 문제:
   - 환경 변수 누락
   - requirements.txt 오류

### 도메인 연결 문제

1. DNS 전파 확인: https://www.whatsmydns.net/
2. Vercel에서 도메인 상태 확인
3. Cloudflare DNS 레코드 확인

---

## 다음 단계 (배포 완료 후)

✅ 배포가 완료되면:

1. **관리자 로그인 테스트**
   - https://mukbang.life/docs 에서 API 문서 확인
   - 로그인 테스트

2. **첫 게시글 작성**
   - API를 통해 게시글 작성
   - 또는 프론트엔드 개발

3. **Google AdSense 설정**
   - [Google AdSense](https://www.google.com/adsense) 가입
   - 도메인 추가
   - 승인 대기

4. **콘텐츠 작성**
   - 블로그 글 작성 시작
   - SEO 최적화

---

## 자세한 가이드

더 자세한 내용은 다음 파일을 참고하세요:
- **[VERCEL_DEPLOY_STEPS.md](VERCEL_DEPLOY_STEPS.md)** - 상세한 배포 가이드
- **[WORDPRESS_DOMAIN_GUIDE.md](WORDPRESS_DOMAIN_GUIDE.md)** - WordPress 도메인 상세 가이드

---

**지금 바로 1단계부터 시작하세요!** 🚀

