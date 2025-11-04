# Cloudflare 설정 가이드 - mukbang.life

WordPress에서 구매한 `mukbang.life` 도메인을 Cloudflare로 연결하는 단계별 가이드입니다.

## 전체 과정 요약

1. ✅ Cloudflare 가입 및 도메인 추가
2. ✅ 네임서버 확인
3. ✅ WordPress.com에서 네임서버 변경
4. ✅ 네임서버 전파 확인
5. ✅ Vercel 배포 후 DNS 레코드 추가

---

## 1단계: Cloudflare 가입 및 도메인 추가

### 1-1. Cloudflare 가입

1. [Cloudflare 가입 페이지](https://dash.cloudflare.com/sign-up) 접속
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

Cloudflare가 자동으로 현재 DNS 레코드를 스캔합니다.

- 현재 WordPress.com의 DNS 레코드들이 표시됩니다
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
   첫 번째: violet.ns.cloudflare.com (예시)
   두 번째: walt.ns.cloudflare.com (예시)
   ```
   (실제 네임서버는 Cloudflare에서 확인한 주소를 입력하세요)
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

## 4단계: Vercel 배포 후 DNS 레코드 추가

### 4-1. Vercel 배포 완료 후

Vercel에서 배포가 완료되고 도메인을 추가한 후:

1. Vercel 프로젝트 → **Settings** → **Domains**
2. `mukbang.life` 도메인 추가
3. Vercel이 DNS 레코드를 제공합니다

### 4-2. Cloudflare에 DNS 레코드 추가

네임서버 전파가 완료된 후 (보통 10분~2시간):

1. [Cloudflare 대시보드](https://dash.cloudflare.com) 접속
2. `mukbang.life` 선택
3. 왼쪽 메뉴에서 **"DNS"** 클릭
4. **"Add record"** 클릭

#### 루트 도메인 (@) 설정

**방법 1: CNAME 레코드 (권장)**
- **Type**: `CNAME`
- **Name**: `@` (또는 비워두기)
- **Target**: `cname.vercel-dns.com` (Vercel에서 제공한 주소)
- **Proxy status**: 🟠 **Proxied** (주황색 구름) ⭐
- **TTL**: Auto
- **"Save"** 클릭

⚠️ **참고**: Cloudflare Free 플랜에서는 `@`에 CNAME을 직접 사용할 수 없을 수 있습니다. 이 경우 방법 2를 사용하세요.

**방법 2: A 레코드 (루트 도메인용)**
- Vercel이 IP 주소를 제공하는 경우:
  - **Type**: `A`
  - **Name**: `@`
  - **IPv4 address**: Vercel에서 제공한 IP 주소
  - **Proxy status**: 🟠 **Proxied**
  - **TTL**: Auto

#### www 서브도메인 설정

- **Type**: `CNAME`
- **Name**: `www`
- **Target**: `cname.vercel-dns.com` (또는 Vercel에서 제공한 주소)
- **Proxy status**: 🟠 **Proxied** (주황색 구름)
- **TTL**: Auto
- **"Save"** 클릭

### 4-3. DNS 레코드 확인

설정 완료 후:
- Cloudflare DNS 메뉴에서 레코드 확인
- Vercel에서 도메인 상태 확인

---

## 5단계: SSL/TLS 설정 (자동)

### 5-1. Cloudflare SSL 설정

1. Cloudflare → **SSL/TLS** 메뉴
2. **Encryption mode**: **Full (strict)** 선택 ⭐
3. **Always Use HTTPS**: 켜기
4. 자동으로 SSL 인증서가 설정됩니다

### 5-2. Vercel SSL

Vercel도 자동으로 SSL 인증서를 제공하므로, Cloudflare에서 **Full (strict)** 모드로 설정하면 됩니다.

---

## 6단계: 완료 확인

### 6-1. 도메인 접속 확인

잠시 후 (몇 분~1시간):

```bash
# 브라우저에서 확인
https://mukbang.life
https://www.mukbang.life
```

### 6-2. DNS 확인

```bash
# DNS 레코드 확인
dig mukbang.life
nslookup mukbang.life
```

### 6-3. SSL 확인

- [SSL Labs 테스트](https://www.ssllabs.com/ssltest/)
- 도메인 입력 후 테스트

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

### DNS 레코드가 작동하지 않는 경우

**원인:**
- 네임서버 전파가 완료되지 않음
- DNS 레코드 타입 또는 값이 잘못됨

**해결:**
1. 네임서버 전파 확인
2. Cloudflare DNS 레코드 확인
3. Vercel에서 도메인 상태 확인
4. TTL을 낮춰서 설정 (600초)

### Cloudflare에서 루트 도메인(@) 설정이 안 되는 경우

**해결:**
1. **방법 1**: Cloudflare의 **Page Rules** 사용
   - Cloudflare → Rules → Page Rules
   - `mukbang.life/*` → Forwarding URL → `https://www.mukbang.life/$1`
   
2. **방법 2**: Vercel에서 루트 도메인 지원 확인
   - Vercel은 루트 도메인을 자동으로 처리합니다

3. **방법 3**: A 레코드 사용 (Vercel이 IP 제공하는 경우)

### WordPress.com에서 네임서버 설정을 찾을 수 없는 경우

**해결:**
1. WordPress.com 도움말 검색: "change nameservers"
2. [WordPress.com 지원](https://wordpress.com/support/domains/)에 문의
3. 도메인 관리 페이지에서 "Advanced" 또는 "고급 설정" 확인

---

## 유용한 도구

- **DNS 전파 확인**: https://www.whatsmydns.net/
- **네임서버 확인**: `dig NS mukbang.life`
- **DNS 레코드 확인**: `dig mukbang.life`
- **SSL 확인**: https://www.ssllabs.com/ssltest/
- **Cloudflare DNS 확인**: Cloudflare 대시보드 → DNS 메뉴

---

## 체크리스트

- [ ] Cloudflare 가입
- [ ] 도메인 추가 (`mukbang.life`)
- [ ] Free 플랜 선택
- [ ] 네임서버 확인 (복사)
- [ ] WordPress.com 로그인
- [ ] 네임서버 변경
- [ ] 네임서버 전파 확인 (10분~2시간 대기)
- [ ] Vercel 배포 완료
- [ ] Vercel에서 도메인 추가
- [ ] Cloudflare에 DNS 레코드 추가
- [ ] SSL/TLS 설정 (Full strict)
- [ ] 도메인 접속 확인

---

## 다음 단계

Cloudflare 설정이 완료되면:

1. ✅ Vercel 배포
2. ✅ Vercel에서 도메인 연결
3. ✅ DNS 레코드 추가
4. ✅ https://mukbang.life 접속 확인

---

## 참고

- **Cloudflare Free 플랜**: 무료, CDN, SSL, DDoS 보호 포함
- **네임서버 전파**: 보통 10분~2시간, 최대 48시간
- **DNS 레코드**: 변경 후 즉시 적용 (TTL에 따라 다름)
- **SSL**: Cloudflare와 Vercel 모두 자동 제공

준비되셨나요? 1단계부터 시작하세요! 🚀

