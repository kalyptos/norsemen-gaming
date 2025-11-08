"""Post management service"""
from typing import List, Optional
from datetime import datetime
from app.models.post import PostCreate, PostUpdate, Post
from app.services.git_service import git_service
from app.config import settings
import re


class PostService:
    """Service for managing blog posts"""

    def __init__(self):
        self.git = git_service

    def generate_frontmatter(self, post_data: dict) -> str:
        """Generate Hugo frontmatter from post data"""
        frontmatter = "---\n"
        frontmatter += f'title: "{post_data["title"]}"\n'
        frontmatter += f'date: {post_data["date"]}\n'
        frontmatter += f'author: "{post_data["author"]}"\n'

        # Categories
        if post_data.get("categories"):
            cats = ", ".join([f'"{c}"' for c in post_data["categories"]])
            frontmatter += f'categories: [{cats}]\n'
        else:
            frontmatter += 'categories: []\n'

        # Tags
        if post_data.get("tags"):
            tags_list = ", ".join([f'"{t}"' for t in post_data["tags"]])
            frontmatter += f'tags: [{tags_list}]\n'
        else:
            frontmatter += 'tags: []\n'

        # Featured image
        if post_data.get("featured"):
            frontmatter += f'featured: "{post_data["featured"]}"\n'

        # Description
        frontmatter += f'description: "{post_data.get("description", "")}"\n'

        # Draft status
        frontmatter += f'draft: {str(post_data.get("draft", True)).lower()}\n'

        frontmatter += "---\n\n"
        return frontmatter

    def slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug"""
        text = text.lower()
        text = re.sub(r'[æåä]', 'a', text)
        text = re.sub(r'[øö]', 'o', text)
        text = re.sub(r'[^a-z0-9]+', '-', text)
        text = text.strip('-')
        return text

    async def create_post(self, post: PostCreate, author_name: str = "CMS Admin") -> dict:
        """Create a new blog post"""

        # Generate slug from title
        slug = self.slugify(post.title)

        # Create file path: content/posts/{game}/{slug}/index.md
        file_path = f"{settings.content_path}/{post.game}/{slug}/index.md"

        # Generate post content
        post_data = {
            "title": post.title,
            "date": datetime.now().isoformat(),
            "author": post.author,
            "categories": post.categories,
            "tags": post.tags,
            "featured": post.featured,
            "description": post.description,
            "draft": post.draft
        }

        frontmatter = self.generate_frontmatter(post_data)
        full_content = frontmatter + post.content

        # Commit to repository
        commit_message = f"Create post: {post.title}"
        result = await self.git.create_file(
            file_path=file_path,
            content=full_content,
            commit_message=commit_message,
            author_name=author_name
        )

        if result["success"]:
            return {
                "success": True,
                "slug": slug,
                "file_path": file_path,
                "url": result.get("url"),
                "message": f"Post '{post.title}' created successfully"
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error")
            }

    async def update_post(
        self,
        game: str,
        slug: str,
        updates: PostUpdate,
        author_name: str = "CMS Admin"
    ) -> dict:
        """Update an existing blog post"""

        file_path = f"{settings.content_path}/{game}/{slug}/index.md"

        # Get existing content
        existing_content = await self.git.get_file_content(file_path)
        if not existing_content:
            return {"success": False, "error": "Post not found"}

        # Parse existing frontmatter
        parts = existing_content.split("---", 2)
        if len(parts) < 3:
            return {"success": False, "error": "Invalid post format"}

        existing_body = parts[2].strip()

        # Parse existing frontmatter (basic parsing)
        post_data = self._parse_frontmatter(parts[1])

        # Update with new values
        if updates.title:
            post_data["title"] = updates.title
        if updates.author:
            post_data["author"] = updates.author
        if updates.categories is not None:
            post_data["categories"] = updates.categories
        if updates.tags is not None:
            post_data["tags"] = updates.tags
        if updates.featured is not None:
            post_data["featured"] = updates.featured
        if updates.description is not None:
            post_data["description"] = updates.description
        if updates.draft is not None:
            post_data["draft"] = updates.draft

        content_body = updates.content if updates.content else existing_body

        # Generate new content
        frontmatter = self.generate_frontmatter(post_data)
        full_content = frontmatter + content_body

        # Commit changes
        commit_message = f"Update post: {post_data['title']}"
        result = await self.git.update_file(
            file_path=file_path,
            content=full_content,
            commit_message=commit_message,
            author_name=author_name
        )

        if result["success"]:
            return {
                "success": True,
                "message": f"Post updated successfully",
                "url": result.get("url")
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error")
            }

    async def delete_post(self, game: str, slug: str, author_name: str = "CMS Admin") -> dict:
        """Delete a blog post"""

        file_path = f"{settings.content_path}/{game}/{slug}/index.md"

        commit_message = f"Delete post: {slug}"
        result = await self.git.delete_file(
            file_path=file_path,
            commit_message=commit_message,
            author_name=author_name
        )

        if result["success"]:
            return {
                "success": True,
                "message": f"Post '{slug}' deleted successfully"
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error")
            }

    def _parse_frontmatter(self, frontmatter: str) -> dict:
        """Basic frontmatter parser"""
        data = {}
        for line in frontmatter.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"')

                if key in ["categories", "tags"]:
                    # Parse list
                    value = value.strip("[]").split(",")
                    value = [v.strip().strip('"') for v in value if v.strip()]

                elif key == "draft":
                    value = value.lower() == "true"

                data[key] = value

        return data


post_service = PostService()
