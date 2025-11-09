"""Git service for GitHub and Gitea integration"""
import base64
from typing import Optional, Dict, Any
from datetime import datetime
import httpx
from github import Github, GithubException
from app.config import settings


class GitService:
    """Service for Git operations (GitHub/Gitea)"""

    def __init__(self):
        self.provider = settings.git_provider.lower()
        self.enabled = False

        if self.provider == "github":
            if settings._github_token and settings._github_repo:
                try:
                    # Parse GitHub URL if provided (extract owner/repo)
                    repo = self._parse_github_repo(settings._github_repo)

                    self.github = Github(settings._github_token)
                    self.repo = self.github.get_repo(repo)
                    self.branch = settings._github_branch
                    self.enabled = True
                    print(f"✓ GitHub integration enabled for {repo}")
                except GithubException as e:
                    print(f"ERROR: Failed to connect to GitHub: {e.data.get('message', str(e))}")
                    print("Git features disabled. Check your GIT_TOKEN and GIT_REPO.")
                except Exception as e:
                    print(f"ERROR: Failed to initialize GitHub: {e}")
                    print("Git features disabled.")
            else:
                print("WARNING: GitHub token or repo not configured. Git features disabled.")
        elif self.provider == "gitea":
            if settings._gitea_token and settings._gitea_repo:
                self.gitea_url = settings.gitea_url.rstrip("/")
                self.gitea_token = settings._gitea_token
                self.gitea_repo = settings._gitea_repo
                self.branch = settings._gitea_branch
                self.enabled = True
            else:
                print("WARNING: Gitea token or repo not configured. Git features disabled.")
        else:
            raise ValueError(f"Unsupported git provider: {self.provider}")

    def _parse_github_repo(self, repo: str) -> str:
        """Parse GitHub repo URL or return owner/repo format"""
        # Remove .git suffix
        repo = repo.rstrip('.git')

        # If it's a URL, extract owner/repo
        if 'github.com/' in repo:
            parts = repo.split('github.com/')[-1].split('/')
            if len(parts) >= 2:
                return f"{parts[0]}/{parts[1]}"

        # Return as-is if already in owner/repo format
        return repo

    async def create_file(
        self,
        file_path: str,
        content: str,
        commit_message: str,
        author_name: str = "CMS Admin",
        author_email: str = "cms@norsemen.ovh"
    ) -> Dict[str, Any]:
        """Create a new file in the repository"""
        if not self.enabled:
            return {"success": False, "error": "Git integration not configured"}

        if self.provider == "github":
            return await self._github_create_file(
                file_path, content, commit_message, author_name, author_email
            )
        else:
            return await self._gitea_create_file(
                file_path, content, commit_message, author_name, author_email
            )

    async def update_file(
        self,
        file_path: str,
        content: str,
        commit_message: str,
        author_name: str = "CMS Admin",
        author_email: str = "cms@norsemen.ovh"
    ) -> Dict[str, Any]:
        """Update an existing file in the repository"""
        if not self.enabled:
            return {"success": False, "error": "Git integration not configured"}

        if self.provider == "github":
            return await self._github_update_file(
                file_path, content, commit_message, author_name, author_email
            )
        else:
            return await self._gitea_update_file(
                file_path, content, commit_message, author_name, author_email
            )

    async def delete_file(
        self,
        file_path: str,
        commit_message: str,
        author_name: str = "CMS Admin",
        author_email: str = "cms@norsemen.ovh"
    ) -> Dict[str, Any]:
        """Delete a file from the repository"""
        if not self.enabled:
            return {"success": False, "error": "Git integration not configured"}

        if self.provider == "github":
            return await self._github_delete_file(
                file_path, commit_message, author_name, author_email
            )
        else:
            return await self._gitea_delete_file(
                file_path, commit_message, author_name, author_email
            )

    async def get_file_content(self, file_path: str) -> Optional[str]:
        """Get file content from repository"""
        if not self.enabled:
            return None

        if self.provider == "github":
            return await self._github_get_file(file_path)
        else:
            return await self._gitea_get_file(file_path)

    # GitHub specific methods
    async def _github_create_file(
        self, file_path: str, content: str, commit_message: str,
        author_name: str, author_email: str
    ) -> Dict[str, Any]:
        """Create file using GitHub API"""
        try:
            result = self.repo.create_file(
                path=file_path,
                message=commit_message,
                content=content,
                branch=self.branch
            )
            return {
                "success": True,
                "sha": result["commit"].sha,
                "url": result["content"].html_url
            }
        except GithubException as e:
            return {"success": False, "error": str(e)}

    async def _github_update_file(
        self, file_path: str, content: str, commit_message: str,
        author_name: str, author_email: str
    ) -> Dict[str, Any]:
        """Update file using GitHub API"""
        try:
            file = self.repo.get_contents(file_path, ref=self.branch)
            result = self.repo.update_file(
                path=file_path,
                message=commit_message,
                content=content,
                sha=file.sha,
                branch=self.branch
            )
            return {
                "success": True,
                "sha": result["commit"].sha,
                "url": result["content"].html_url
            }
        except GithubException as e:
            return {"success": False, "error": str(e)}

    async def _github_delete_file(
        self, file_path: str, commit_message: str,
        author_name: str, author_email: str
    ) -> Dict[str, Any]:
        """Delete file using GitHub API"""
        try:
            file = self.repo.get_contents(file_path, ref=self.branch)
            result = self.repo.delete_file(
                path=file_path,
                message=commit_message,
                sha=file.sha,
                branch=self.branch
            )
            return {"success": True, "sha": result["commit"].sha}
        except GithubException as e:
            return {"success": False, "error": str(e)}

    async def _github_get_file(self, file_path: str) -> Optional[str]:
        """Get file content from GitHub"""
        try:
            file = self.repo.get_contents(file_path, ref=self.branch)
            return file.decoded_content.decode("utf-8")
        except GithubException:
            return None

    # Gitea specific methods
    async def _gitea_create_file(
        self, file_path: str, content: str, commit_message: str,
        author_name: str, author_email: str
    ) -> Dict[str, Any]:
        """Create file using Gitea API"""
        url = f"{self.gitea_url}/api/v1/repos/{self.gitea_repo}/contents/{file_path}"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers={"Authorization": f"token {self.gitea_token}"},
                json={
                    "content": base64.b64encode(content.encode()).decode(),
                    "message": commit_message,
                    "branch": self.branch,
                    "author": {"name": author_name, "email": author_email}
                }
            )

            if response.status_code in [200, 201]:
                data = response.json()
                return {
                    "success": True,
                    "sha": data["commit"]["sha"],
                    "url": data["content"]["html_url"]
                }
            else:
                return {"success": False, "error": response.text}

    async def _gitea_update_file(
        self, file_path: str, content: str, commit_message: str,
        author_name: str, author_email: str
    ) -> Dict[str, Any]:
        """Update file using Gitea API"""
        # First get the file SHA
        file_content = await self._gitea_get_file_info(file_path)
        if not file_content:
            return {"success": False, "error": "File not found"}

        url = f"{self.gitea_url}/api/v1/repos/{self.gitea_repo}/contents/{file_path}"

        async with httpx.AsyncClient() as client:
            response = await client.put(
                url,
                headers={"Authorization": f"token {self.gitea_token}"},
                json={
                    "content": base64.b64encode(content.encode()).decode(),
                    "message": commit_message,
                    "sha": file_content["sha"],
                    "branch": self.branch,
                    "author": {"name": author_name, "email": author_email}
                }
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "sha": data["commit"]["sha"],
                    "url": data["content"]["html_url"]
                }
            else:
                return {"success": False, "error": response.text}

    async def _gitea_delete_file(
        self, file_path: str, commit_message: str,
        author_name: str, author_email: str
    ) -> Dict[str, Any]:
        """Delete file using Gitea API"""
        file_content = await self._gitea_get_file_info(file_path)
        if not file_content:
            return {"success": False, "error": "File not found"}

        url = f"{self.gitea_url}/api/v1/repos/{self.gitea_repo}/contents/{file_path}"

        async with httpx.AsyncClient() as client:
            response = await client.delete(
                url,
                headers={"Authorization": f"token {self.gitea_token}"},
                json={
                    "message": commit_message,
                    "sha": file_content["sha"],
                    "branch": self.branch,
                    "author": {"name": author_name, "email": author_email}
                }
            )

            if response.status_code == 200:
                return {"success": True}
            else:
                return {"success": False, "error": response.text}

    async def _gitea_get_file(self, file_path: str) -> Optional[str]:
        """Get file content from Gitea"""
        file_info = await self._gitea_get_file_info(file_path)
        if file_info and "content" in file_info:
            return base64.b64decode(file_info["content"]).decode("utf-8")
        return None

    async def _gitea_get_file_info(self, file_path: str) -> Optional[Dict]:
        """Get file info (including SHA) from Gitea"""
        url = f"{self.gitea_url}/api/v1/repos/{self.gitea_repo}/contents/{file_path}"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"token {self.gitea_token}"},
                params={"ref": self.branch}
            )

            if response.status_code == 200:
                return response.json()
            return None


# Singleton instance
git_service = GitService()
