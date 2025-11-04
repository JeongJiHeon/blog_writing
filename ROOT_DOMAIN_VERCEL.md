# mukbang.life 루트 도메인을 Vercel로 연결하기

WordPress.com에서 관리 중인 `mukbang.life` 루트 도메인을 Vercel로 연결하는 방법입니다.

## 현재 상황

- ✅ `www.mukbang.life` → Vercel로 연결됨
- ❌ `mukbang.life` → WordPress.com에서 관리 중 (수정 불가)

## 해결 방법: 네임서버를 Cloudflare로 변경

WordPress.com에서 A 레코드를 수정할 수 없으므로, 네임서버를 Cloudflare로 변경해야 합니다.

---

## 전체 과정 (5단계)

1. ✅ Cloudflare 가입 및 도메인 추가
2. ✅ 네임서버 확인
3. ✅ WordPress.com에서 네임서버 변경
4. ✅ 네임서버 전파 확인
5. ✅ Cloudflare에서 DNS 레코드 설정 (루트 도메인 + www)

---

## 1단계: Cloudflare 가입 및 도메인 추가

### 1-1. Cloudflare 가입

1. [Cloudflare 가입](https://dash.cloudflare.com/sign-up)
2. 이메일 주소 입력 후 **"Sign Up"** 클릭
3. 이메일 인증 완료
4. 로그인

### 1-2. 도메인 추가

1. Cloudflare 대시보드에서 **"Add a Site"** 클릭
2. 도메인 입력: `mukbang.life`
3. **"Add site"** 클릭
4. 플랜 선택: **Free** 플랜 선택 (무료)
5. **"Continue"** 클릭

### 1-3. DNS 레코드 스캔

Cloudflare가 자동으로 현재 DNS 레코드를 스캔합니다:
- 현재 WordPress.com의 레코드들이 표시됩니다
- 확인 후 **"Continue"** 클릭

### 1-4. 네임서버 확인 ⭐ 중요!

Cloudflare가 2개의 네임서버를 제공합니다:

```
예시:
violet.ns.cloudflare.com
walt.ns.cloudflare.com
```

⚠️ **이 네임서버 주소를 복사해두세요!** (실제 주소는 Cloudflare에서 확인하세요)

---

## 2단계: WordPress.com에서 네임서버 변경

### 2-1. WordPress.com 로그인

1. [WordPress.com](https://wordpress.com) 로그인
2. 계정 메뉴 클릭

### 2-2. 도메인 설정 페이지로 이동

**방법 1:**
1. **"Domains"** 또는 **"도메인"** 메뉴 클릭
2. `mukbang.life` 도메인 찾기
3. 도메인 클릭

**방법 2:**
1. 직접 URL 접속: https://wordpress.com/domains/manage/mukbang.life

### 2-3. 네임서버 변경

도메인 설정 페이지에서:

1. **"Nameservers"** 또는 **"네임서버"** 또는 **"DNS"** 메뉴 찾기
2. **"Change nameservers"** 또는 **"네임서버 변경"** 클릭
3. **"Use custom nameservers"** 또는 **"사용자 정의 네임서버 사용"** 선택
4. Cloudflare에서 받은 네임서버 2개 입력:
   ```
   첫 번째: violet.ns.cloudflare.com (예시 - 실제는 Cloudflare에서 확인)
   두 번째: walt.ns.cloudflare.com (예시 - 실제는 Cloudflare에서 확인)
   ```
5. **"Save"** 또는 **"저장"** 클릭

### 2-4. 확인 메시지

WordPress.com에서 네임서버 변경 완료 메시지가 표시됩니다.

⚠️ **주의**: 네임서버 변경은 최대 24-48시간이 걸릴 수 있지만, 보통 10분~2시간 내에 완료됩니다.

---

## 3단계: 네임서버 전파 확인

### 3-1. 전파 상태 확인

네임서버 변경이 완료되었는지 확인:

1. [DNS 전파 확인 도구](https://www.whatsmydns.net/#NS/mukbang.life) 접속
2. 전 세계 여러 서버에서 네임서버 확인
3. Cloudflare 네임서버가 표시되면 전파 완료!

### 3-2. 로컬에서 확인 (선택사항)

터미널에서 확인:

```bash
# 네임서버 확인
dig NS mukbang.life

# 또는
nslookup -type=NS mukbang.life
```

Cloudflare 네임서버가 표시되면 성공!

---

## 4단계: Cloudflare에서 DNS 레코드 설정

네임서버 전파가 완료된 후 (보통 10분~2시간):

### 4-1. Cloudflare DNS 메뉴로 이동

1. [Cloudflare 대시보드](https://dash.cloudflare.com) 접속
2. `mukbang.life` 선택
3. 왼쪽 메뉴에서 **"DNS"** 클릭

### 4-2. www 서브도메인용 CNAME 레코드

기존 레코드가 있으면 수정, 없으면 추가:

1. **"Add record"** 클릭
2. 다음 설정:
   - **Type**: `CNAME`
   - **Name**: `www`
   - **Target**: `cname.vercel-dns.com` (또는 Vercel에서 제공한 주소)
   - **Proxy status**: 🔵 **DNS-only** (회색 구름) ⭐
   - **TTL**: Auto
3. **"Save"** 클릭

### 4-3. 루트 도메인(@)용 CNAME 레코드

1. **"Add record"** 클릭
2. 다음 설정:
   - **Type**: `CNAME`
   - **Name**: `@` (또는 비워두기)
   - **Target**: `cname.vercel-dns.com` (Vercel에서 제공한 주소)
   - **Proxy status**: 🔵 **DNS-only** (회색 구름) ⭐
   - **TTL**: Auto
3. **"Save"** 클릭

⚠️ **참고**: Cloudflare Free 플랜에서는 `@`에 CNAME을 직접 사용할 수 없을 수 있습니다. 이 경우:
- Cloudflare는 자동으로 A 레코드로 변환하거나
- Vercel이 IP 주소를 제공하면 A 레코드를 사용

### 4-4. 기존 레코드 확인

이메일 관련 레코드가 있다면 유지:
- MX 레코드 (이메일 서버)
- TXT 레코드 (SPF, DKIM 등)

---

## 5단계: Vercel에서 도메인 설정

### 5-1. 루트 도메인 추가

1. Vercel 프로젝트 → **Settings** → **Domains**
2. `mukbang.life` 추가 (이미 추가되어 있다면 설정 확인)
3. **"Connect to an environment"** 선택
4. 드롭다운: **"Production"** 선택
5. **"Save"** 클릭

### 5-2. www 서브도메인 확인

1. `www.mukbang.life` 확인
2. **"Connect to an environment"** → **"Production"** 선택되어 있는지 확인

---

## 6단계: 완료 확인

### 6-1. DNS 레코드 확인

```bash
# 루트 도메인 확인
dig mukbang.life

# www 서브도메인 확인
dig CNAME www.mukbang.life
```

### 6-2. 도메인 접속 테스트

DNS 전파 완료 후 (10분~2시간):

```bash
# 브라우저에서 확인
https://mukbang.life
https://www.mukbang.life
```

두 도메인 모두 Vercel 블로그가 표시되어야 합니다!

### 6-3. Vercel에서 상태 확인

1. Vercel → Settings → Domains
2. `mukbang.life` 상태 확인
3. `www.mukbang.life` 상태 확인
4. 둘 다 "Valid Configuration"으로 표시되어야 합니다

---

## 문제 해결

### 네임서버 변경이 적용되지 않는 경우

**원인:**
- 전파 시간이 더 필요함 (최대 48시간)
- 네임서버 주소가 잘못 입력됨

**해결:**
1. [DNS 전파 확인](https://www.whatsmydns.net/#NS/mukbang.life)에서 전파 상태 확인
2. WordPress.com에서 네임서버 주소 다시 확인
3. 시간이 지난 후 다시 확인

### Cloudflare에서 루트 도메인(@) CNAME이 안 되는 경우

**해결책:**
1. **방법 1**: Cloudflare가 자동으로 처리
   - CNAME을 추가하면 Cloudflare가 자동으로 A 레코드로 변환
   
2. **방법 2**: Vercel IP 주소 사용
   - Vercel에서 IP 주소를 제공하는 경우
   - A 레코드로 직접 설정

3. **방법 3**: Page Rules 사용
   - Cloudflare → Rules → Page Rules
   - `mukbang.life/*` → Forwarding URL → `https://www.mukbang.life/$1`

### WordPress.com에서 네임서버 설정을 찾을 수 없는 경우

**해결:**
1. WordPress.com 도움말 검색: "change nameservers"
2. [WordPress.com 지원](https://wordpress.com/support/domains/)에 문의
3. 도메인 관리 페이지에서 "Advanced" 또는 "고급 설정" 확인

---

## 체크리스트

### Cloudflare 설정
- [ ] Cloudflare 가입
- [ ] 도메인 추가 (`mukbang.life`)
- [ ] Free 플랜 선택
- [ ] 네임서버 확인 (복사)

### WordPress.com 설정
- [ ] WordPress.com 로그인
- [ ] 도메인 설정 페이지로 이동
- [ ] 네임서버 변경
- [ ] Cloudflare 네임서버 입력
- [ ] 저장

### 네임서버 전파
- [ ] 네임서버 전파 확인 (10분~2시간 대기)
- [ ] 전파 완료 확인

### Cloudflare DNS 설정
- [ ] DNS 메뉴로 이동
- [ ] www용 CNAME 레코드 추가
- [ ] 루트 도메인(@)용 CNAME 레코드 추가
- [ ] Proxy status: DNS-only 설정

### Vercel 설정
- [ ] 루트 도메인 추가 (`mukbang.life`)
- [ ] Production 환경에 연결
- [ ] www 서브도메인 확인

### 완료 확인
- [ ] DNS 레코드 확인
- [ ] https://mukbang.life 접속 테스트
- [ ] https://www.mukbang.life 접속 테스트
- [ ] Vercel에서 도메인 상태 확인

---

## 다음 단계

설정이 완료되면:

1. ✅ 두 도메인 모두 Vercel 블로그로 연결
2. ✅ SSL 인증서 자동 설정
3. ✅ 블로그 사용 시작!

---

## 참고

- **네임서버 전파 시간**: 보통 10분~2시간, 최대 48시간
- **DNS 레코드 전파**: 네임서버 전파 후 거의 즉시
- **이메일 서비스**: 네임서버 변경 시 WordPress.com Titan 이메일 사용 불가 (다른 이메일 서비스 필요)

준비되셨나요? 1단계부터 시작하세요! 🚀

