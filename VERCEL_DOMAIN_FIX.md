# Vercel 도메인 설정 오류 해결 가이드

"Invalid Configuration" 오류가 발생하는 경우 해결 방법입니다.

## 문제 상황

Vercel에서 도메인 설정 시 "Invalid Configuration" 오류가 발생하는 이유:
1. DNS 레코드가 아직 설정되지 않음
2. DNS 전파가 완료되지 않음
3. 도메인 설정이 잘못됨

## 해결 방법

### 방법 1: 두 도메인 모두 Production에 연결 (권장)

#### 1단계: www.mukbang.life 설정

1. `www.mukbang.life` 도메인 섹션에서:
   - ✅ **"Connect to an environment"** 선택
   - 드롭다운: **"Production"** 선택
   - **"Save"** 클릭

#### 2단계: mukbang.life 설정

1. `mukbang.life` 도메인 섹션에서:
   - ✅ **"Connect to an environment"** 선택
   - 드롭다운: **"Production"** 선택
   - **"Redirect to Another Domain"** 선택 해제
   - **"Save"** 클릭

이렇게 하면 두 도메인 모두 Production 환경에 연결됩니다.

---

### 방법 2: 루트 도메인을 www로 리다이렉트 (대안)

#### 1단계: www.mukbang.life 설정

1. `www.mukbang.life` 도메인 섹션에서:
   - ✅ **"Connect to an environment"** 선택
   - 드롭다운: **"Production"** 선택
   - **"Save"** 클릭

#### 2단계: mukbang.life 리다이렉트 설정

1. `mukbang.life` 도메인 섹션에서:
   - ✅ **"Redirect to Another Domain"** 선택
   - Redirect type: **"307 Temporary Redirect"** (또는 308 Permanent)
   - Redirect to: `www.mukbang.life` 입력
   - **"Save"** 클릭

이렇게 하면 `mukbang.life`는 `www.mukbang.life`로 리다이렉트됩니다.

---

## DNS 설정 확인

### 1. Cloudflare DNS 레코드 설정

Vercel에서 도메인 설정 후, Cloudflare에 DNS 레코드를 추가해야 합니다.

1. Cloudflare 대시보드 → **DNS** 메뉴
2. **"Add record"** 클릭

#### www.mukbang.life용 CNAME 레코드

- **Type**: `CNAME`
- **Name**: `www`
- **Target**: `cname.vercel-dns.com` (또는 Vercel에서 제공한 주소)
- **Proxy status**: 🟠 **Proxied** (주황색 구름)
- **TTL**: Auto
- **Save**

#### mukbang.life (루트 도메인)용 레코드

**옵션 A: CNAME 레코드 (권장)**
- **Type**: `CNAME`
- **Name**: `@`
- **Target**: `cname.vercel-dns.com`
- **Proxy status**: 🟠 **Proxied**
- **TTL**: Auto

**옵션 B: A 레코드 (CNAME이 안 되는 경우)**
- Vercel에서 IP 주소를 제공하는 경우:
  - **Type**: `A`
  - **Name**: `@`
  - **IPv4 address**: Vercel에서 제공한 IP
  - **Proxy status**: 🟠 **Proxied**

### 2. DNS 전파 확인

DNS 레코드 추가 후:
- [DNS 전파 확인](https://www.whatsmydns.net/#CNAME/www.mukbang.life)
- 전파 시간: 보통 10분~2시간

### 3. Vercel에서 도메인 상태 확인

DNS 전파가 완료되면:
1. Vercel → Settings → Domains
2. 도메인 상태가 "Valid Configuration"으로 변경됩니다
3. "Invalid Configuration" 오류가 사라집니다

---

## 단계별 체크리스트

### Vercel 설정
- [ ] `www.mukbang.life` → Production 환경에 연결
- [ ] `mukbang.life` → Production 환경에 연결 (또는 www로 리다이렉트)
- [ ] 두 도메인 모두 "Save" 클릭

### Cloudflare DNS 설정
- [ ] Cloudflare에 로그인
- [ ] DNS 메뉴로 이동
- [ ] www.mukbang.life용 CNAME 레코드 추가
- [ ] mukbang.life용 CNAME 또는 A 레코드 추가
- [ ] Proxy status: Proxied 설정

### 확인
- [ ] DNS 전파 확인 (10분~2시간 대기)
- [ ] Vercel에서 도메인 상태 확인
- [ ] https://mukbang.life 접속 테스트
- [ ] https://www.mukbang.life 접속 테스트

---

## 문제 해결

### "Invalid Configuration" 오류가 계속 나타나는 경우

**원인 1: DNS 레코드 미설정**
- Cloudflare에 DNS 레코드가 추가되었는지 확인
- Vercel에서 제공한 정확한 주소를 사용했는지 확인

**원인 2: DNS 전파 미완료**
- 전파에 시간이 걸립니다 (최대 48시간)
- [DNS 전파 확인 도구](https://www.whatsmydns.net/)로 확인

**원인 3: 잘못된 DNS 레코드**
- CNAME 타겟이 정확한지 확인
- Proxy status가 올바르게 설정되었는지 확인

**원인 4: 네임서버 미변경**
- WordPress.com에서 네임서버가 Cloudflare로 변경되었는지 확인
- [네임서버 확인](https://www.whatsmydns.net/#NS/mukbang.life)

### Vercel에서 도메인을 제거하고 다시 추가

1. Vercel → Settings → Domains
2. 도메인 옆 **"Remove"** 클릭
3. 잠시 후 다시 추가
4. DNS 레코드 확인 후 **"Save"** 클릭

---

## 현재 권장 설정

### 설정 방법 (권장)

1. **www.mukbang.life**:
   - Connect to an environment → Production
   - Save

2. **mukbang.life**:
   - Connect to an environment → Production
   - Save

이렇게 하면 두 도메인 모두 동일한 사이트에 연결됩니다.

### Cloudflare DNS 레코드

```
Type: CNAME
Name: www
Target: cname.vercel-dns.com (또는 Vercel에서 제공한 주소)
Proxy: Proxied

Type: CNAME
Name: @
Target: cname.vercel-dns.com
Proxy: Proxied
```

---

## 다음 단계

1. ✅ Vercel에서 도메인 설정 수정
2. ✅ Cloudflare에 DNS 레코드 추가
3. ✅ DNS 전파 대기 (10분~2시간)
4. ✅ 도메인 접속 확인

DNS 설정이 완료되면 "Invalid Configuration" 오류가 사라집니다! 🚀

