"""
블로그 애플리케이션 설정
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 데이터베이스
    database_url: str = "sqlite:///./blog.db"
    
    # JWT 설정
    secret_key: str = "your-secret-key-here-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24시간
    
    # 관리자 계정
    admin_username: str = "admin"
    admin_password: str = "admin123"
    
    # 블로그 설정
    blog_title: str = "My Blog"
    blog_description: str = "Welcome to my blog"
    
    # 미디어 설정
    upload_dir: str = "uploads"
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

