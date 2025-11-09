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
    git_token: str = ""  # Universal token for both providers
    git_repo: str = ""   # Universal repo for both providers
    git_branch: str = "main"  # Universal branch for both providers

    # GitHub (legacy - prefer GIT_TOKEN)
    github_token: str = ""
    github_repo: str = ""
    github_branch: str = "main"

    # Gitea
    gitea_url: str = ""
    gitea_token: str = ""
    gitea_repo: str = ""
    gitea_branch: str = "main"

    @property
    def _github_token(self) -> str:
        """Get GitHub token from GIT_TOKEN or GITHUB_TOKEN"""
        return self.git_token or self.github_token

    @property
    def _github_repo(self) -> str:
        """Get GitHub repo from GIT_REPO or GITHUB_REPO"""
        return self.git_repo or self.github_repo

    @property
    def _github_branch(self) -> str:
        """Get GitHub branch from GIT_BRANCH or GITHUB_BRANCH"""
        return self.git_branch or self.github_branch

    @property
    def _gitea_token(self) -> str:
        """Get Gitea token from GIT_TOKEN or GITEA_TOKEN"""
        return self.git_token or self.gitea_token

    @property
    def _gitea_repo(self) -> str:
        """Get Gitea repo from GIT_REPO or GITEA_REPO"""
        return self.git_repo or self.gitea_repo

    @property
    def _gitea_branch(self) -> str:
        """Get Gitea branch from GIT_BRANCH or GITEA_BRANCH"""
        return self.git_branch or self.gitea_branch

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
