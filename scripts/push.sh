#!/bin/bash

# GitHub 푸시 스크립트
cd "$(dirname "$0")/.."

# .env 파일 확인
if [ ! -f .env ]; then
    echo "❌ .env 파일이 없습니다."
    echo "python scripts/setup_env.py 를 실행하여 .env 파일을 생성하세요."
    exit 1
fi

# .env 파일 로드
source .env

# Python 스크립트 실행
python3 scripts/github_push.py

