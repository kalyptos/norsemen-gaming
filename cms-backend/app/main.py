"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.config import settings
from app.routers import auth, posts, uploads
import os


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="CMS Backend for Norsemen Gaming Blog"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# Templates
templates_path = os.path.join(os.path.dirname(__file__), "..", "templates")
templates = Jinja2Templates(directory=templates_path)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(posts.router, prefix="/api")
app.include_router(uploads.router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve admin UI"""
    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "app_name": settings.app_name}
    )


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "git_provider": settings.git_provider
    }


@app.get("/api/info")
async def info():
    """Get CMS information"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "git_provider": settings.git_provider,
        "repo": settings.github_repo if settings.git_provider == "github" else settings.gitea_repo
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
