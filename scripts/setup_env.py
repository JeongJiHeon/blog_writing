"""
.env 파일 설정 스크립트
"""
import os
from pathlib import Path

def create_env_file():
    """환경 변수 입력 받아서 .env 파일 생성"""
    env_path = Path(__file__).parent.parent / '.env'
    
    if env_path.exists():
        response = input("⚠️  .env 파일이 이미 존재합니다. 덮어쓰시겠습니까? (y/n): ")
        if response.lower() != 'y':
            print("취소되었습니다.")
            return
    
    print("\n📝 환경 변수 설정을 시작합니다...\n")
    
    # GitHub 설정
    print("=== GitHub 설정 ===")
    github_token = input("GitHub Token: ").strip()
    github_username = input("GitHub Username: ").strip()
    github_repo = input("GitHub Repository 이름 (기본: blog_writing): ").strip() or "blog_writing"
    
    # 애플리케이션 설정
    print("\n=== 애플리케이션 설정 ===")
    secret_key = input("SECRET_KEY (엔터 시 자동 생성): ").strip()
    if not secret_key:
        import secrets
        secret_key = secrets.token_urlsafe(32)
        print(f"생성된 SECRET_KEY: {secret_key}")
    
    admin_username = input("관리자 사용자명 (기본: admin): ").strip() or "admin"
    admin_password = input("관리자 비밀번호: ").strip()
    if not admin_password:
        print("⚠️  경고: 비밀번호가 설정되지 않았습니다. 기본값을 사용합니다.")
        admin_password = "admin123"
    
    database_url = input("DATABASE_URL (기본: sqlite:///./blog.db): ").strip() or "sqlite:///./blog.db"
    
    # .env 파일 작성
    env_content = f"""# GitHub 설정
GITHUB_TOKEN={github_token}
GITHUB_USERNAME={github_username}
GITHUB_REPO={github_repo}

# 애플리케이션 설정 (Vercel 배포 시 사용)
SECRET_KEY={secret_key}
ADMIN_USERNAME={admin_username}
ADMIN_PASSWORD={admin_password}
DATABASE_URL={database_url}
"""
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ .env 파일이 생성되었습니다: {env_path}")
    print("\n다음 명령어로 GitHub에 푸시하세요:")
    print("  python scripts/github_push.py")

if __name__ == "__main__":
    create_env_file()

