# DNS 레코드 설정 후 확인 가이드

WordPress.com에서 DNS 레코드를 수정하셨다면, 다음 단계를 확인하세요.

## 1단계: DNS 전파 확인

DNS 레코드 변경 후 전파 시간이 필요합니다 (보통 10분~2시간).

### 온라인 도구로 확인

1. [DNS 전파 확인 도구](https://www.whatsmydns.net/) 접속
2. 도메인 입력: `www.mukbang.life`
3. 레코드 타입: `CNAME` 선택
4. 전파 상태 확인

### 터미널에서 확인

```bash
# CNAME 레코드 확인
dig CNAME www.mukbang.life

# 또는
nslookup -type=CNAME www.mukbang.life
```

전파가 완료되면 Vercel 주소가 표시됩니다.

---

## 2단계: Vercel에서 도메인 상태 확인

### 확인 방법

1. Vercel 대시보드 접속
2. 프로젝트 선택
3. **Settings** → **Domains** 메뉴
4. 도메인 상태 확인

### 정상 상태

- ✅ "Valid Configuration" (녹색)
- ✅ "DNS Verified" 또는 "Active"

### 여전히 오류가 있는 경우

- ❌ "Invalid Configuration" (빨간색)
- ❌ "DNS Not Configured"

---

## 3단계: Vercel 도메인 설정 확인

### www.mukbang.life 설정

1. `www.mukbang.life` 도메인 섹션 확인
2. **"Connect to an environment"** 선택되어 있는지 확인
3. 드롭다운: **"Production"** 선택
4. **"Save"** 클릭 (변경사항이 있다면)

### mukbang.life 설정

두 가지 옵션:

**옵션 A: Production에 연결 (권장)**
- ✅ **"Connect to an environment"** 선택
- 드롭다운: **"Production"** 선택
- **"Save"** 클릭

**옵션 B: www로 리다이렉트**
- ✅ **"Redirect to Another Domain"** 선택
- Redirect type: **"307 Temporary Redirect"**
- Redirect to: `www.mukbang.life`
- **"Save"** 클릭

---

## 4단계: 설정한 DNS 레코드 확인

WordPress.com에서 설정한 레코드가 올바른지 확인:

### 확인 사항

1. **www.mukbang.life용 CNAME 레코드**
   - Type: `CNAME`
   - Name: `www`
   - Value: Vercel에서 제공한 주소 (예: `cname.vercel-dns.com`)
   - TTL: 3600 (또는 기본값)

2. **mukbang.life (루트 도메인) 레코드**
   - A 레코드 또는 CNAME 레코드
   - Vercel 주소로 설정

---

## 5단계: 도메인 접속 테스트

### DNS 전파 완료 후 (10분~2시간)

브라우저에서 확인:

```
https://www.mukbang.life
https://mukbang.life
```

### 정상 작동 확인

- ✅ 사이트가 정상적으로 로드됨
- ✅ SSL 인증서가 정상 작동 (자물쇠 아이콘)
- ✅ Vercel 배포된 사이트가 표시됨

---

## 문제 해결

### "Invalid Configuration" 오류가 계속 나타나는 경우

**원인 1: DNS 전파 미완료**
- 전파에 시간이 걸립니다 (최대 48시간)
- [DNS 전파 확인 도구](https://www.whatsmydns.net/)로 확인

**원인 2: DNS 레코드 오류**
- 레코드 타입이 올바른지 확인 (CNAME 또는 A)
- 타겟 주소가 정확한지 확인
- Vercel에서 제공한 정확한 주소 사용

**원인 3: Vercel 도메인 설정 오류**
- 두 도메인 모두 Production에 연결되어 있는지 확인
- "Save" 버튼을 클릭했는지 확인

### DNS 레코드는 설정했는데 여전히 오류가 있는 경우

1. **DNS 전파 대기** (10분~2시간)
2. **Vercel에서 도메인 재설정**:
   - 도메인 제거 후 다시 추가
   - 또는 "Save" 버튼 다시 클릭
3. **DNS 레코드 다시 확인**:
   - WordPress.com에서 설정한 레코드 확인
   - 타겟 주소가 정확한지 확인

---

## 다음 단계

DNS 전파가 완료되면:

1. ✅ Vercel에서 도메인 상태 확인
2. ✅ 도메인 접속 테스트
3. ✅ 블로그 사용 시작!

---

## 확인 명령어

### DNS 레코드 확인

```bash
# www 서브도메인 확인
dig CNAME www.mukbang.life

# 루트 도메인 확인
dig mukbang.life

# 모든 레코드 확인
dig mukbang.life ANY
```

### Vercel 연결 확인

```bash
# Vercel 앱 URL로 직접 접속
curl -I https://your-app.vercel.app

# 도메인으로 접속
curl -I https://www.mukbang.life
```

---

준비되셨나요? DNS 전파를 기다린 후 Vercel에서 도메인 상태를 확인하세요! 🚀

