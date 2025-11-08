# Norsemen Gaming CMS Backend

FastAPI-based CMS for managing blog posts with GitHub/Gitea integration.

## Features

- 🔐 JWT authentication
- 📝 Create, update, and delete blog posts
- 📸 Image upload support
- 🔄 Direct GitHub/Gitea integration (auto-commits)
- 🎨 Modern admin UI with markdown editor
- 🚀 RESTful API

## Quick Start

### 1. Install Dependencies

```bash
cd cms-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and configure:
- `SECRET_KEY` - Generate a random secret key
- `ADMIN_USERNAME` and `ADMIN_PASSWORD`
- `GITHUB_TOKEN` and `GITHUB_REPO` (or Gitea equivalents)

### 3. Run the Server

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
python app/main.py
```

### 4. Access Admin UI

Open http://localhost:8000 in your browser and login with your admin credentials.

## API Endpoints

### Authentication
- `POST /api/auth/login` - Get access token
- `GET /api/auth/me` - Get current user info

### Posts
- `POST /api/posts/` - Create new post
- `PUT /api/posts/{game}/{slug}` - Update post
- `DELETE /api/posts/{game}/{slug}` - Delete post

### Uploads
- `POST /api/uploads/image` - Upload image

## GitHub/Gitea Setup

### GitHub

1. Create a Personal Access Token:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` scope
   - Copy token to `.env` as `GITHUB_TOKEN`

2. Set `GITHUB_REPO` to `username/repo-name`

### Gitea

1. Create Application Token in Gitea settings
2. Configure `.env`:
   ```
   GIT_PROVIDER=gitea
   GITEA_URL=https://your-gitea-instance.com
   GITEA_TOKEN=your-token
   GITEA_REPO=username/repo-name
   ```

## Architecture

```
cms-backend/
├── app/
│   ├── main.py           # FastAPI application
│   ├── config.py         # Settings management
│   ├── models/           # Pydantic models
│   ├── routers/          # API endpoints
│   │   ├── auth.py
│   │   ├── posts.py
│   │   └── uploads.py
│   └── services/         # Business logic
│       ├── auth_service.py
│       ├── git_service.py
│       └── post_service.py
├── templates/
│   └── admin.html        # Admin UI
├── static/               # Static assets
└── requirements.txt
```

## Post Structure

Posts are created as Hugo page bundles:
```
content/posts/
└── {game}/
    └── {slug}/
        ├── index.md
        └── feature.jpg
```

Frontmatter format:
```yaml
---
title: "Post Title"
date: 2025-01-08T10:00:00+02:00
author: "Norsemen"
categories: ["Gaming"]
tags: ["space", "multiplayer"]
featured: "feature.jpg"
description: "SEO description"
draft: false
---

Post content here...
```

## Security Notes

- **IMPORTANT**: Change `SECRET_KEY` and `ADMIN_PASSWORD` in production
- Use HTTPS in production
- Keep GitHub/Gitea tokens secure
- Never commit `.env` file to repository

## Deployment

### Docker (recommended)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t norsemen-cms .
docker run -p 8000:8000 --env-file .env norsemen-cms
```

### Traditional Deployment

Use a process manager like systemd, supervisor, or PM2:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Troubleshooting

### "Could not validate credentials"
- Check if your GitHub/Gitea token is valid
- Ensure token has correct permissions

### "File already exists"
- Post with that slug already exists
- Choose a different title or manually edit the slug

### Image upload fails
- Check file size (max 5MB)
- Verify GitHub/Gitea token has write access
- Ensure image format is supported

## License

MIT
