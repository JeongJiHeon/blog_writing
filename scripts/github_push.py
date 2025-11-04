"""
GitHub 푸시 자동화 스크립트
"""
import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_REPO = os.getenv('GITHUB_REPO', 'blog_writing')

if not GITHUB_TOKEN:
    print("❌ 오류: GITHUB_TOKEN이 .env 파일에 설정되지 않았습니다.")
    sys.exit(1)

if not GITHUB_USERNAME:
    print("❌ 오류: GITHUB_USERNAME이 .env 파일에 설정되지 않았습니다.")
    sys.exit(1)

def run_command(cmd, check=True):
    """명령어 실행"""
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ 오류: {e}")
        print(f"출력: {e.stdout}")
        print(f"에러: {e.stderr}")
        if check:
            sys.exit(1)
        return None

def main():
    """GitHub에 푸시"""
    print("🚀 GitHub 푸시 시작...")
    
    # 현재 디렉토리 확인
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Git 상태 확인
    print("\n1️⃣ Git 상태 확인 중...")
    status = run_command("git status", check=False)
    if "nothing to commit" not in status:
        print("📝 변경사항이 있습니다. 커밋을 진행합니다...")
        run_command("git add .")
        run_command('git commit -m "Update: Auto commit"')
    else:
        print("✅ 커밋할 변경사항이 없습니다.")
    
    # 원격 저장소 확인 및 설정
    print("\n2️⃣ 원격 저장소 확인 중...")
    remote_url = run_command("git remote get-url origin", check=False)
    
    if not remote_url or GITHUB_USERNAME not in remote_url:
        # 원격 저장소 URL 설정
        repo_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"
        print(f"🔗 원격 저장소 설정: {GITHUB_USERNAME}/{GITHUB_REPO}")
        
        # 기존 원격 저장소 제거 (있는 경우)
        run_command("git remote remove origin", check=False)
        
        # 새 원격 저장소 추가
        run_command(f'git remote add origin {repo_url}')
    else:
        # 토큰이 포함된 URL로 업데이트
        repo_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"
        run_command(f'git remote set-url origin {repo_url}')
        print(f"✅ 원격 저장소 업데이트: {GITHUB_USERNAME}/{GITHUB_REPO}")
    
    # 브랜치 확인
    print("\n3️⃣ 브랜치 확인 중...")
    current_branch = run_command("git branch --show-current")
    if current_branch != "main":
        run_command("git branch -M main")
    
    # 푸시
    print("\n4️⃣ GitHub에 푸시 중...")
    try:
        run_command("git push -u origin main")
        print("\n✅ 푸시 완료!")
        print(f"📦 저장소: https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}")
    except Exception as e:
        print(f"\n❌ 푸시 실패: {e}")
        print("\n💡 해결 방법:")
        print("1. GitHub 저장소가 이미 생성되어 있는지 확인하세요")
        print("2. GitHub 토큰이 올바른 권한을 가지고 있는지 확인하세요")
        print("3. 저장소 이름이 정확한지 확인하세요")
        sys.exit(1)

if __name__ == "__main__":
    main()

