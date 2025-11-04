#!/bin/bash

# 블로그 배포 스크립트
# 사용법: ./deploy.sh [서버_IP] [도메인]

set -e

SERVER_IP=${1:-""}
DOMAIN=${2:-""}

if [ -z "$SERVER_IP" ] || [ -z "$DOMAIN" ]; then
    echo "사용법: ./deploy.sh <서버_IP> <도메인>"
    echo "예시: ./deploy.sh 203.0.113.1 yourdomain.com"
    exit 1
fi

echo "=== 블로그 배포 시작 ==="
echo "서버 IP: $SERVER_IP"
echo "도메인: $DOMAIN"
echo ""

# 1. 서버 IP 확인
echo "1. 서버 IP 확인 중..."
if ping -c 1 "$SERVER_IP" > /dev/null 2>&1; then
    echo "✓ 서버에 연결 가능합니다"
else
    echo "✗ 서버에 연결할 수 없습니다. IP 주소를 확인하세요."
    exit 1
fi

# 2. DNS 확인
echo ""
echo "2. DNS 설정 확인 중..."
DNS_RESULT=$(dig +short "$DOMAIN" @8.8.8.8)
if [ -z "$DNS_RESULT" ]; then
    echo "⚠ 경고: DNS 레코드가 아직 설정되지 않았거나 전파되지 않았습니다."
    echo "   도메인 제공업체에서 다음 A 레코드를 설정하세요:"
    echo "   @  A  $SERVER_IP  3600"
    echo "   www  A  $SERVER_IP  3600"
else
    echo "✓ DNS 설정 확인됨: $DNS_RESULT"
    if [ "$DNS_RESULT" != "$SERVER_IP" ]; then
        echo "⚠ 경고: DNS IP($DNS_RESULT)가 서버 IP($SERVER_IP)와 일치하지 않습니다."
    fi
fi

# 3. 포트 확인
echo ""
echo "3. 서버 포트 확인 중..."
if nc -z -v -w5 "$SERVER_IP" 22 2>/dev/null; then
    echo "✓ SSH 포트(22) 열려있음"
else
    echo "✗ SSH 포트(22)에 연결할 수 없습니다."
    exit 1
fi

if nc -z -v -w5 "$SERVER_IP" 80 2>/dev/null; then
    echo "✓ HTTP 포트(80) 열려있음"
else
    echo "⚠ HTTP 포트(80)가 닫혀있습니다. Nginx 설정이 필요할 수 있습니다."
fi

if nc -z -v -w5 "$SERVER_IP" 443 2>/dev/null; then
    echo "✓ HTTPS 포트(443) 열려있음"
else
    echo "⚠ HTTPS 포트(443)가 닫혀있습니다. SSL 인증서 설정이 필요합니다."
fi

echo ""
echo "=== 배포 준비 완료 ==="
echo ""
echo "다음 단계:"
echo "1. 서버에 SSH로 접속하여 애플리케이션 배포"
echo "2. Nginx 설정 (필요한 경우)"
echo "3. SSL 인증서 설정 (Let's Encrypt)"
echo "4. 방화벽 설정 확인"
echo ""
echo "배포 명령어 예시:"
echo "  ssh root@$SERVER_IP"
echo "  git clone <your-repo-url>"
echo "  cd blog_writing"
echo "  pip install -r requirements.txt"
echo "  uvicorn main:app --host 0.0.0.0 --port 8000"

