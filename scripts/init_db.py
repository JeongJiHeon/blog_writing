"""
데이터베이스 초기화 스크립트
Heroku 배포 시 자동으로 실행됩니다.
"""

from database import init_db
from models import User
from database import SessionLocal
from auth import get_password_hash
from config import settings

if __name__ == "__main__":
    print("데이터베이스 초기화 중...")
    init_db()
    print("데이터베이스 초기화 완료!")
    
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == settings.admin_username).first()
        if not admin:
            print("관리자 계정 생성 중...")
            admin = User(
                username=settings.admin_username,
                email=f"{settings.admin_username}@example.com",
                hashed_password=get_password_hash(settings.admin_password),
                is_admin=True
            )
            db.add(admin)
            db.commit()
            print(f"관리자 계정 생성 완료: {settings.admin_username}")
        else:
            print("관리자 계정이 이미 존재합니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

