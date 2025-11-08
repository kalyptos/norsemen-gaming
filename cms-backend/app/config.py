"""Configuration management for CMS Backend"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Application
    app_name: str = "Norsemen Gaming CMS"
    app_version: str = "1.0.0"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 720

    # Admin credentials
    admin_username: str = "admin"
    admin_password: str  # Hashed in production

    # Git Provider
    git_provider: str = "github"  # github or gitea

    # GitHub
    github_token: str = ""
    github_repo: str = ""
    github_branch: str = "main"

    # Gitea
    gitea_url: str = ""
    gitea_token: str = ""
    gitea_repo: str = ""
    gitea_branch: str = "main"

    # Paths
    content_path: str = "content/posts"
    images_path: str = "static/images/uploads"

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:8000"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
