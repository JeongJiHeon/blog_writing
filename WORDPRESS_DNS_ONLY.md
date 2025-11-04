# WordPress.com에서 DNS 레코드만 변경하기 (네임서버 변경 없이)

WordPress.com의 네임서버를 그대로 사용하면서 DNS 레코드만 변경하는 방법입니다.

## 제한사항 확인

⚠️ **중요**: WordPress.com에서 구매한 도메인은 네임서버를 변경하지 않으면 DNS 레코드 수정이 **제한적**입니다.

WordPress.com에서 직접 DNS 레코드를 수정할 수 있는지 먼저 확인해야 합니다.

---

## 방법 1: WordPress.com에서 직접 DNS 레코드 수정 (가능한 경우)

### 1단계: WordPress.com DNS 설정 확인

1. [WordPress.com](https://wordpress.com) 로그인
2. **도메인** 메뉴 클릭
3. `mukbang.life` 도메인 선택
4. **"DNS"** 또는 **"DNS Records"** 또는 **"도메인 설정"** 메뉴 찾기

### 2단계: DNS 레코드 확인

현재 DNS 레코드가 보이는지 확인:
- A 레코드
- CNAME 레코드
- MX 레코드
- TXT 레코드

### 3단계: DNS 레코드 수정 (가능한 경우)

Vercel 배포 후:

1. WordPress.com DNS 설정 페이지에서
2. **"Add Record"** 또는 **"레코드 추가"** 클릭

#### www.mukbang.life용 CNAME 레코드 추가

- **Type**: `CNAME`
- **Name**: `www`
- **Value**: `cname.vercel-dns.com` (Vercel에서 제공한 주소)
- **TTL**: 3600 (또는 기본값)

#### mukbang.life (루트 도메인)용 레코드

⚠️ **문제**: WordPress.com에서는 루트 도메인(`@`)에 CNAME을 직접 사용할 수 없을 수 있습니다.

**해결책:**
1. **A 레코드 사용** (Vercel이 IP 주소를 제공하는 경우)
   - Type: `A`
   - Name: `@`
   - Value: Vercel에서 제공한 IP 주소

2. **www로 리다이렉트** (WordPress.com 기능 사용)
   - `mukbang.life` → `www.mukbang.life`로 리다이렉트 설정

---

## 방법 2: WordPress.com에서 네임서버 변경 (권장)

네임서버를 변경하면 Cloudflare에서 DNS를 완전히 제어할 수 있습니다.

### 장점
- ✅ 모든 DNS 레코드 자유롭게 수정 가능
- ✅ Cloudflare CDN 사용 가능
- ✅ 무료 SSL 인증서
- ✅ 더 빠른 DNS 응답

### 단점
- ⚠️ WordPress.com의 이메일 서비스(Titan) 사용 불가 (다른 이메일 서비스 필요)

### 설정 방법

1. **Cloudflare 설정** (이전 가이드 참고)
2. **WordPress.com에서 네임서버 변경**
   - WordPress.com → 도메인 → `mukbang.life` 선택
   - 네임서버를 Cloudflare 네임서버로 변경
3. **Cloudflare에서 DNS 레코드 관리**

---

## 방법 3: WordPress.com에서 제한적으로 DNS 관리 (대안)

### 현재 설정 확인

WordPress.com에서 다음을 확인하세요:

1. **DNS 레코드 수정 가능 여부**
   - DNS 메뉴에서 레코드 추가/수정이 가능한지 확인

2. **A 레코드 수정 가능 여부**
   - 현재 `@` → WordPress.com에서 처리 중인 A 레코드
   - 이 레코드를 수정할 수 있는지 확인

### 가능한 설정

WordPress.com에서 직접 수정이 가능한 경우:

```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

그리고 WordPress.com의 리다이렉트 기능을 사용하여:
- `mukbang.life` → `www.mukbang.life`로 리다이렉트

---

## 추천 방법

### 상황별 추천

1. **WordPress.com에서 DNS 레코드 수정이 가능한 경우**
   → **방법 1**: WordPress.com에서 직접 수정

2. **WordPress.com에서 DNS 레코드 수정이 불가능한 경우**
   → **방법 2**: 네임서버를 Cloudflare로 변경 (권장)

3. **이메일 서비스를 계속 사용해야 하는 경우**
   → **방법 3**: 제한적으로 관리하거나 www 서브도메인만 사용

---

## 실제 설정 방법

### WordPress.com에서 DNS 레코드 확인

1. WordPress.com 로그인
2. 도메인 → `mukbang.life` 선택
3. **"DNS"** 또는 **"DNS Records"** 메뉴 찾기

### 확인 사항

다음 중 어떤 것이 가능한지 확인:

- [ ] DNS 레코드 추가/수정 가능
- [ ] A 레코드 수정 가능
- [ ] CNAME 레코드 추가 가능
- [ ] 루트 도메인(@) 레코드 수정 가능

### 가능한 경우 설정

WordPress.com에서 DNS 레코드를 수정할 수 있다면:

1. **www 서브도메인용 CNAME 추가**:
   ```
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com (Vercel에서 제공한 주소)
   ```

2. **루트 도메인 처리**:
   - A 레코드 수정 (Vercel IP 사용)
   - 또는 WordPress.com 리다이렉트 기능 사용

---

## 문제 해결

### WordPress.com에서 DNS 레코드를 찾을 수 없는 경우

**원인**: WordPress.com은 네임서버를 변경하지 않으면 DNS 레코드 수정이 제한적일 수 있습니다.

**해결책**:
1. WordPress.com 고객 지원에 문의
2. 또는 네임서버를 Cloudflare로 변경 (권장)

### 루트 도메인(@) 레코드를 수정할 수 없는 경우

**해결책**:
1. www 서브도메인만 사용
2. WordPress.com의 리다이렉트 기능 사용
3. 또는 네임서버 변경하여 Cloudflare에서 관리

---

## 다음 단계

1. WordPress.com에서 DNS 설정 메뉴 확인
2. DNS 레코드 수정 가능 여부 확인
3. 가능한 경우: WordPress.com에서 직접 수정
4. 불가능한 경우: 네임서버 변경 고려

---

## 체크리스트

- [ ] WordPress.com 로그인
- [ ] 도메인 설정 페이지 확인
- [ ] DNS 메뉴 찾기
- [ ] DNS 레코드 수정 가능 여부 확인
- [ ] 가능한 경우: 레코드 추가/수정
- [ ] 불가능한 경우: 네임서버 변경 고려

---

**참고**: WordPress.com에서 DNS 레코드 수정이 제한적인 경우, 네임서버를 Cloudflare로 변경하는 것이 가장 안정적이고 유연한 방법입니다.

