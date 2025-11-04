# WordPress에서 구매한 도메인 사용하기

WordPress에서 구매한 도메인을 우리 블로그 시스템에 연결하는 방법을 안내합니다.

## 상황 확인

먼저 어떤 경우인지 확인해주세요:

### 1. WordPress.com에서 커스텀 도메인 구매
- WordPress.com 계정에서 도메인을 구매한 경우
- WordPress.com 블로그에 연결되어 있는 경우

### 2. WordPress.org 사용 중 + 도메인 업체에서 구매
- WordPress.org를 직접 설치해서 사용 중
- 도메인 업체(가비아, 후이즈 등)에서 구매

## 방법 1: WordPress.com에서 구매한 도메인 사용하기

### 옵션 A: WordPress.com에서 도메인 연결 해제 (권장)

WordPress.com에서 구매한 도메인도 네임서버를 변경하여 다른 곳에서 사용할 수 있습니다.

#### 1단계: WordPress.com 도메인 설정 확인

1. WordPress.com 로그인
2. **도메인** → 구매한 도메인 선택
3. **도메인 설정** 또는 **DNS** 메뉴 확인

#### 2단계: 네임서버 변경

WordPress.com에서 네임서버를 변경하여 다른 DNS 제공업체를 사용할 수 있습니다:

**Cloudflare 사용 (무료, 추천):**
1. [Cloudflare](https://www.cloudflare.com) 가입
2. 도메인 추가
3. Cloudflare에서 제공하는 네임서버 확인 (예: `nameserver1.cloudflare.com`, `nameserver2.cloudflare.com`)
4. WordPress.com에서 네임서버 변경:
   - WordPress.com → 도메인 → DNS 설정
   - 네임서버를 Cloudflare의 네임서버로 변경

**또는 도메인 제공업체 직접 사용:**
- WordPress.com에서 네임서버를 도메인 제공업체의 네임서버로 변경
- 도메인 제공업체에서 DNS 레코드 직접 관리

#### 3단계: DNS 레코드 설정

네임서버 변경 후, DNS 레코드를 설정합니다:

**Heroku 배포 시:**
```
www   CNAME   your-app.herokuapp.com
@     ALIAS   your-app.herokuapp.com
```

**직접 서버 배포 시:**
```
@     A       서버_IP_주소
www   A       서버_IP_주소
```

### 옵션 B: WordPress.com에서 도메인 이전 (고급)

Word메인을 완전히 다른 업체로 이전할 수도 있습니다. 이 경우:
1. WordPress.com에서 도메인 이전 코드(Authorization Code) 발급
2. 원하는 도메인 업체로 이전
3. 새 업체에서 DNS 설정

⚠️ **주의**: 이전에는 시간이 걸리고 추가 비용이 발생할 수 있습니다.

## 방법 2: WordPress.org + 도메인 업체에서 구매한 경우

이 경우는 가장 간단합니다. 도메인 업체에서 직접 DNS 설정을 변경하면 됩니다.

### 1단계: 도메인 업체 로그인

구매한 도메인 업체(가비아, 후이즈, GoDaddy 등)에 로그인

### 2단계: DNS 관리 페이지로 이동

- **가비아**: 나의 도메인 → 도메인 선택 → DNS 관리
- **후이즈**: 도메인 관리 → 도메인 선택 → DNS 관리
- **GoDaddy**: My Products → 도메인 → DNS

### 3단계: DNS 레코드 설정

배포 방법에 따라 설정:

**Heroku 사용 시:**
```
타입      호스트    값
CNAME     www      your-app.herokuapp.com
ALIAS     @        your-app.herokuapp.com
```

**직접 서버 사용 시:**
```
타입      호스트    값
A         @        서버_IP_주소
A         www      서버_IP_주소
```

## 단계별 가이드

### WordPress.com에서 구매한 도메인을 Cloudflare로 연결

#### 1. Cloudflare 설정

1. [Cloudflare](https://dash.cloudflare.com/sign-up) 가입
2. **Add a Site** 클릭
3. 도메인 입력 (예: `yourdomain.com`)
4. 플랜 선택 (Free 플랜 선택)
5. DNS 레코드 확인/스캔

#### 2. Cloudflare 네임서버 확인

Cloudflare에서 다음 네임서버를 제공합니다:
```
nameserver1.cloudflare.com
nameserver2.cloudflare.com
```

#### 3. WordPress.com에서 네임서버 변경

1. WordPress.com 로그인
2. **도메인** 메뉴
3. 구매한 도메인 선택
4. **도메인 설정** 또는 **고급 설정**
5. **네임서버 변경** 또는 **DNS 설정**
6. Cloudflare의 네임서버로 변경
   - 네임서버 1: `nameserver1.cloudflare.com`
   - 네임서버 2: `nameserver2.cloudflare.com`
7. 저장

⚠️ **네임서버 변경은 24-48시간이 걸릴 수 있습니다.**

#### 4. Cloudflare에서 DNS 레코드 설정

네임서버 전파 후 (확인: https://www.whatsmydns.net/):

**Heroku 배포 시:**
1. Cloudflare 대시보드 → DNS 메뉴
2. 레코드 추가:
   - **타입**: `CNAME`
   - **이름**: `www`
   - **타겟**: `your-app.herokuapp.com`
   - **프록시**: 꺼짐 (회색 구름) 또는 켜짐 (주황색 구름)
3. 루트 도메인(@) 설정:
   - Cloudflare에서 `@`는 CNAME으로 설정 불가
   - **방법 1**: ALIAS 레코드 사용 (Business 플랜 이상)
   - **방법 2**: Page Rules 사용
   - **방법 3**: Heroku에서 루트 도메인 지원 확인

**직접 서버 배포 시:**
1. Cloudflare 대시보드 → DNS 메뉴
2. 레코드 추가:
   - **타입**: `A`
   - **이름**: `@` (또는 비워두기)
   - **IPv4 주소**: 서버 IP 주소
   - **프록시**: 꺼짐 (처음에는 꺼짐으로, SSL 설정 후 켜기)
3. www 서브도메인 추가:
   - **타입**: `CNAME`
   - **이름**: `www`
   - **타겟**: `yourdomain.com`
   - **프록시**: 켜짐

#### 5. SSL/TLS 설정 (Cloudflare)

1. Cloudflare → SSL/TLS 메뉴
2. **Encryption mode**: Full (strict) 또는 Full
3. **Always Use HTTPS**: 켜기

### WordPress.com에서 직접 DNS 관리 (제한적)

WordPress.com에서도 일부 DNS 레코드를 관리할 수 있습니다:

1. WordPress.com → 도메인 → DNS 설정
2. A 레코드 또는 CNAME 레코드 추가
3. **제한사항**: WordPress.com은 일부 DNS 기능이 제한적일 수 있음

## WordPress.com 도메인 연결 해제 확인

### 현재 상태 확인

```bash
# 현재 네임서버 확인
dig NS yourdomain.com

# 현재 DNS 레코드 확인
dig yourdomain.com
nslookup yourdomain.com
```

### WordPress.com 네임서버 확인

일반적으로 WordPress.com의 네임서버는:
- `ns1.wordpress.com`
- `ns2.wordpress.com`
- `ns3.wordpress.com`

만약 이 네임서버가 보이면, WordPress.com에서 관리 중입니다.

## 문제 해결

### 네임서버 변경이 적용되지 않는 경우

1. **전파 시간 대기**: 최대 48시간 소요 가능
2. **캐시 확인**: https://www.whatsmydns.net/ 에서 전 세계 전파 상태 확인
3. **로컬 DNS 캐시 클리어**:
   ```bash
   # macOS
   sudo dscacheutil -flushcache
   
   # Windows
   ipconfig /flushdns
   ```

### WordPress.com에서 도메인 설정을 찾을 수 없는 경우

1. WordPress.com 고객 지원에 문의
2. 도메인이 WordPress.com에서 완전히 관리되는지 확인
3. 도메인 이전 옵션 확인

### DNS 레코드가 작동하지 않는 경우

1. TTL 값을 낮춰서 설정 (600초 등)
2. 레코드 타입 확인 (A vs CNAME)
3. 오타 확인 (IP 주소, 도메인명)
4. 시간이 지난 후 다시 확인

## 추천 방법

### 가장 쉬운 방법 (초보자 추천)

1. **Cloudflare 사용**:
   - 무료
   - 빠른 DNS 전파
   - 자동 SSL 인증서
   - CDN 기능

2. **단계**:
   - Cloudflare 가입
   - 도메인 추가
   - WordPress.com에서 네임서버 변경
   - Cloudflare에서 DNS 레코드 설정

### 가장 빠른 방법 (고급 사용자)

1. **도메인 제공업체 직접 사용**:
   - WordPress.com에서 도메인 이전
   - 도메인 업체에서 직접 DNS 관리
   - 더 많은 제어권

## 다음 단계

DNS 설정이 완료되면:

1. **배포**: `DEPLOYMENT.md` 참고하여 블로그 배포
2. **SSL 확인**: HTTPS 작동 여부 확인
3. **테스트**: 도메인으로 접속 테스트

## 유용한 도구

- **DNS 전파 확인**: https://www.whatsmydns.net/
- **네임서버 확인**: `dig NS yourdomain.com`
- **DNS 레코드 확인**: `dig yourdomain.com`
- **SSL 확인**: https://www.ssllabs.com/ssltest/

## FAQ

### Q: WordPress.com에서 도메인을 구매했는데, 완전히 나의 것으로 사용할 수 있나요?

A: 네, 네임서버를 변경하면 다른 곳에서 사용할 수 있습니다. 하지만 WordPress.com의 일부 기능(예: 이메일 호스팅)은 사용하지 못할 수 있습니다.

### Q: WordPress.com 블로그를 사용 중인데, 도메인만 따로 사용할 수 있나요?

A: WordPress.com에서 도메인을 구매했다면, 네임서버를 변경하여 다른 곳에서도 사용할 수 있습니다. 하지만 WordPress.com 블로그와의 연결은 끊어집니다.

### Q: 도메인 이전이 필요한가요?

A: 네임서버만 변경하면 되므로, 완전한 이전은 필요하지 않습니다. 다만, 더 많은 제어권을 원한다면 이전을 고려할 수 있습니다.

### Q: WordPress.com에서 도메인을 구매했는데, 환불이 가능한가요?

A: WordPress.com의 도메인 환불 정책을 확인하세요. 일반적으로 구매 후 일정 기간 내에는 환불이 가능할 수 있습니다.

