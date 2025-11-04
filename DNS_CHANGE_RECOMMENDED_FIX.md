# "DNS Change Recommended" 오류 해결 가이드

Vercel에서 "DNS Change Recommended" 경고가 나타나는 경우 해결 방법입니다.

## 현재 상태 분석

- ✅ `www.mukbang.life`: "DNS Change Recommended" (Production 연결됨)
- ❌ `mukbang.life`: "Invalid Configuration" (www로 리다이렉트)

## 문제 원인

"DNS Change Recommended"는 다음 경우에 발생합니다:

1. **DNS 레코드가 올바르게 설정되지 않음**
2. **Cloudflare Proxy 모드 사용** (Vercel이 DNS-only를 선호)
3. **CNAME 레코드 타겟이 잘못됨**
4. **DNS 전파가 완료되지 않음**

---

## 해결 방법

### 방법 1: Cloudflare Proxy 끄기 (DNS-only 모드) - 권장

Cloudflare의 Proxied 모드가 Vercel과 호환성 문제를 일으킬 수 있습니다.

#### Cloudflare에서 설정 변경

1. [Cloudflare 대시보드](https://dash.cloudflare.com) 접속
2. `mukbang.life` 선택
3. **DNS** 메뉴 클릭
4. `www` CNAME 레코드 찾기
5. **Proxy status**를 **DNS-only** (회색 구름)로 변경
6. **Save** 클릭

#### Vercel에서 확인

1. Vercel 대시보드 → Settings → Domains
2. `www.mukbang.life` 옆 **"Refresh"** 버튼 클릭
3. 몇 분 후 상태 확인

### 방법 2: DNS 레코드 다시 확인

WordPress.com에서 설정한 DNS 레코드 확인:

#### www.mukbang.life용 CNAME 레코드

확인 사항:
- ✅ Type: `CNAME`
- ✅ Name: `www`
- ✅ Value: `cname.vercel-dns.com` (정확한 주소)
- ✅ TTL: 3600 (또는 기본값)

#### Vercel에서 정확한 주소 확인

Vercel → Settings → Domains에서:
- `www.mukbang.life` 도메인 클릭
- "Configuration" 또는 "DNS" 섹션에서
- Vercel이 요구하는 정확한 CNAME 타겟 확인

일반적으로:
- `cname.vercel-dns.com`
- 또는 `cname.vercel-dns.com.` (끝에 점)

### 방법 3: 도메인 재설정

#### Vercel에서 도메인 제거 후 다시 추가

1. Vercel → Settings → Domains
2. `www.mukbang.life` 옆 **"Edit"** 클릭
3. **"Remove"** 클릭
4. 잠시 후 다시 추가:
   - "Add Domain" 클릭
   - `www.mukbang.life` 입력
   - "Connect to an environment" → Production 선택
   - "Save" 클릭

---

## mukbang.life (루트 도메인) 설정

현재 `mukbang.life`는 `www.mukbang.life`로 리다이렉트되도록 설정되어 있습니다.

### 옵션 1: 그대로 유지 (리다이렉트)

- `mukbang.life` → `www.mukbang.life`로 리다이렉트
- "Invalid Configuration" 오류는 무시 가능 (리다이렉트는 작동함)

### 옵션 2: Production에 직접 연결

1. `mukbang.life` 도메인 → **"Edit"** 클릭
2. **"Redirect to Another Domain"** 선택 해제
3. **"Connect to an environment"** 선택
4. 드롭다운: **"Production"** 선택
5. **"Save"** 클릭

이 경우 WordPress.com에서 `mukbang.life`용 DNS 레코드도 설정해야 합니다.

---

## 단계별 해결 가이드

### 1단계: Cloudflare Proxy 끄기

1. Cloudflare → DNS 메뉴
2. `www` CNAME 레코드 찾기
3. Proxy status를 **DNS-only** (회색 구름)로 변경
4. Save

### 2단계: Vercel에서 도메인 새로고침

1. Vercel → Settings → Domains
2. `www.mukbang.life` 옆 **"Refresh"** 버튼 클릭
3. 1-2분 대기

### 3단계: DNS 전파 확인

```bash
# DNS 레코드 확인
dig CNAME www.mukbang.life

# 또는 온라인 도구
# https://www.whatsmydns.net/#CNAME/www.mukbang.life
```

### 4단계: 상태 확인

Vercel에서:
- "DNS Change Recommended" 경고가 사라지는지 확인
- "Valid Configuration"으로 변경되는지 확인

---

## 문제 해결

### "DNS Change Recommended"가 계속 나타나는 경우

**원인 1: DNS 전파 미완료**
- 전파에 시간이 걸립니다 (최대 48시간)
- [DNS 전파 확인](https://www.whatsmydns.net/)으로 확인

**원인 2: Cloudflare Proxy 모드**
- Proxy를 끄고 DNS-only 모드로 변경
- Vercel은 DNS-only 모드를 선호합니다

**원인 3: 잘못된 CNAME 타겟**
- Vercel에서 제공한 정확한 주소 확인
- 끝에 점(.)이 있는지 확인 (`cname.vercel-dns.com.` vs `cname.vercel-dns.com`)

**원인 4: TTL 설정**
- TTL을 낮춰서 설정 (600초)
- 빠른 전파 가능

### Cloudflare Proxy를 꺼야 하나요?

**권장**: 네, Proxy를 끄는 것이 좋습니다.

**이유**:
- Vercel이 DNS-only 모드를 선호
- "DNS Change Recommended" 경고 해결
- Vercel의 자체 CDN과 SSL 사용

**하지만**:
- Proxy를 켜도 작동은 할 수 있습니다
- 다만 경고가 계속 나타날 수 있습니다

---

## 현재 권장 설정

### Cloudflare DNS 레코드

```
Type: CNAME
Name: www
Target: cname.vercel-dns.com (또는 Vercel에서 제공한 정확한 주소)
Proxy status: DNS-only (회색 구름) ⭐
TTL: Auto 또는 600
```

### Vercel 도메인 설정

```
www.mukbang.life:
- Connect to an environment → Production
- Save

mukbang.life:
- Redirect to Another Domain → www.mukbang.life
- 또는 Connect to an environment → Production
```

---

## 확인 방법

### DNS 레코드 확인

```bash
# CNAME 레코드 확인
dig CNAME www.mukbang.life +short

# 예상 결과: cname.vercel-dns.com.
```

### Vercel 상태 확인

1. Vercel → Settings → Domains
2. `www.mukbang.life` 상태 확인
3. "Valid Configuration"으로 변경되었는지 확인

---

## 다음 단계

1. ✅ Cloudflare에서 Proxy 끄기 (DNS-only 모드)
2. ✅ Vercel에서 도메인 새로고침
3. ✅ DNS 전파 대기 (10분~1시간)
4. ✅ 상태 확인

준비되셨나요? Cloudflare에서 Proxy를 끄고 Vercel에서 새로고침해보세요! 🚀

