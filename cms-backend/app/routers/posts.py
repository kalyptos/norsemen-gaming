"""Post management API routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.auth import User
from app.models.post import PostCreate, PostUpdate
from app.services.auth_service import get_current_active_user
from app.services.post_service import post_service


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/")
async def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new blog post"""
    result = await post_service.create_post(post, author_name=current_user.username)

    if result["success"]:
        return {
            "message": result["message"],
            "slug": result["slug"],
            "file_path": result["file_path"],
            "url": result.get("url")
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to create post")
        )


@router.put("/{game}/{slug}")
async def update_post(
    game: str,
    slug: str,
    updates: PostUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update an existing blog post"""
    result = await post_service.update_post(
        game=game,
        slug=slug,
        updates=updates,
        author_name=current_user.username
    )

    if result["success"]:
        return {
            "message": result["message"],
            "url": result.get("url")
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to update post")
        )


@router.delete("/{game}/{slug}")
async def delete_post(
    game: str,
    slug: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a blog post"""
    result = await post_service.delete_post(
        game=game,
        slug=slug,
        author_name=current_user.username
    )

    if result["success"]:
        return {"message": result["message"]}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to delete post")
        )


@router.get("/status")
async def posts_status():
    """Check if posts service is working"""
    return {"status": "ok", "message": "Posts service is running"}
