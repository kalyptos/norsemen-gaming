"""File upload API routes"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from app.models.auth import User
from app.services.auth_service import get_current_active_user
from app.services.git_service import git_service
from app.config import settings
import base64
from datetime import datetime
import re


router = APIRouter(prefix="/uploads", tags=["Uploads"])


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be URL-friendly"""
    # Get file extension
    parts = filename.rsplit(".", 1)
    name = parts[0] if len(parts) > 1 else filename
    ext = parts[1] if len(parts) > 1 else ""

    # Sanitize name
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    name = name.strip('-')

    # Add timestamp to avoid conflicts
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    if ext:
        return f"{name}-{timestamp}.{ext}"
    return f"{name}-{timestamp}"


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    game: str = "general",
    current_user: User = Depends(get_current_active_user)
):
    """Upload an image file"""

    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed"
        )

    # Validate file size (5MB max)
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 5MB"
        )

    # Generate sanitized filename
    safe_filename = sanitize_filename(file.filename)

    # Create file path
    file_path = f"{settings.images_path}/{game}/{safe_filename}"

    # Upload to repository
    commit_message = f"Upload image: {safe_filename}"
    result = await git_service.create_file(
        file_path=file_path,
        content=base64.b64encode(content).decode(),
        commit_message=commit_message,
        author_name=current_user.username
    )

    if result["success"]:
        return {
            "success": True,
            "filename": safe_filename,
            "path": file_path,
            "url": f"/images/uploads/{game}/{safe_filename}",
            "message": "Image uploaded successfully"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to upload image")
        )


@router.get("/status")
async def uploads_status():
    """Check if uploads service is working"""
    return {"status": "ok", "message": "Uploads service is running"}
