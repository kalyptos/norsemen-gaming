# Deployment Guide - Coolify 4 & Docker

This guide covers deploying Norsemen Gaming to Coolify 4 using Docker Compose.

## Prerequisites

- Coolify 4 server (https://coolify.io)
- Git repository access
- GitHub or Gitea Personal Access Token

## Quick Start

1. **Clone repository** in Coolify 4
2. **Set environment variables** (see below)
3. **Deploy** using Docker Compose

Coolify will automatically detect the `docker-compose.yml` file and build both services.

## Environment Variables

Configure these in Coolify 4's environment settings:

### Required Variables

```bash
# Security (IMPORTANT: Generate secure values!)
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ADMIN_PASSWORD=<your-secure-password>

# Git Integration
GIT_PROVIDER=github  # or gitea
GIT_REPO=kalyptos/norsemen-gaming
GIT_TOKEN=<your-personal-access-token>
GIT_BRANCH=main
```

### Optional Variables

```bash
# Ports (Coolify manages these automatically)
FRONTEND_PORT=8080
BACKEND_PORT=8000

# Token Expiry
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (Add your production domain)
ALLOWED_ORIGINS=https://norsemen.ovh,https://api.norsemen.ovh

# Admin Username (default: admin)
ADMIN_USERNAME=admin

# Logging
DEBUG=false
LOG_LEVEL=info
```

## Generate Secrets

### SECRET_KEY
```bash
openssl rand -hex 32
```

### GitHub Personal Access Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control)
4. Copy token and save as `GIT_TOKEN`

### Gitea Personal Access Token
1. Go to your Gitea instance → Settings → Applications
2. Generate new token with repository permissions
3. Copy token and save as `GIT_TOKEN`

## Coolify 4 Setup

### Step 1: Add New Resource
1. In Coolify, click **"+ New Resource"**
2. Select **"Docker Compose"**
3. Choose your Git provider and repository

### Step 2: Configure Build
1. **Docker Compose Location**: `/docker-compose.yml` (auto-detected)
2. **Branch**: `main` (or your branch name)
3. **Build Settings**: Leave default (Coolify handles this)

### Step 3: Set Environment Variables
1. Go to **"Environment Variables"** tab
2. Add all required variables from above
3. Mark `SECRET_KEY`, `GIT_TOKEN`, `ADMIN_PASSWORD` as **sensitive**

### Step 4: Configure Domains
1. **Frontend**: `norsemen.ovh` → Port 8080
2. **Backend** (optional): `api.norsemen.ovh` → Port 8000

### Step 5: Deploy
1. Click **"Deploy"**
2. Wait for build to complete
3. Check logs for any errors

## Architecture

### Services

1. **Frontend** (Hugo + Nginx)
   - Built from root `Dockerfile`
   - Serves static site on port 80 (mapped to 8080)
   - Health check: `http://localhost/health`

2. **Backend** (FastAPI CMS)
   - Built from `cms-backend/Dockerfile`
   - API and admin UI on port 8000
   - Health check: `http://localhost:8000/health`

### Volumes

- `backend-data`: Persistent data storage
- `backend-uploads`: Image uploads

### Network

- `norsemen-network`: Bridge network for inter-service communication

## Accessing the CMS

After deployment:
- **Admin UI**: `https://api.norsemen.ovh/` (or your backend domain)
- **API Docs**: `https://api.norsemen.ovh/docs`
- **Frontend**: `https://norsemen.ovh/`

### First Login
1. Go to admin UI
2. Username: `admin` (or your `ADMIN_USERNAME`)
3. Password: Your `ADMIN_PASSWORD`

## Updating Content

### Via FastAPI CMS
1. Login to admin UI
2. Create/edit posts using the editor
3. Click "Publish" - commits directly to Git
4. Coolify auto-deploys on new commits

### Via Decap CMS
1. Go to `https://norsemen.ovh/admin/`
2. Authenticate with GitHub/Gitea OAuth
3. Create/edit content
4. Publish - commits to Git
5. Coolify auto-deploys

### Manual
1. Edit files in `content/posts/`
2. Commit and push to Git
3. Coolify auto-deploys

## Troubleshooting

### Build Fails
- Check Coolify build logs
- Ensure Hugo version 0.148.2 is being used
- Verify all environment variables are set

### Backend Can't Commit
- Check `GIT_TOKEN` has proper permissions
- Verify `GIT_REPO` format is correct
- Check Git provider (github vs gitea)

### Health Check Fails
- Check service logs in Coolify
- Verify ports are not conflicting
- Ensure health endpoints return 200 OK

### CORS Errors
- Add your domain to `ALLOWED_ORIGINS`
- Format: `https://domain.com,https://api.domain.com`
- No trailing slashes

## Local Development

### With Docker Compose
```bash
# Copy environment file
cp .env.example .env

# Edit .env with your values
nano .env

# Build and run
docker-compose up --build

# Access
# Frontend: http://localhost:8080
# Backend: http://localhost:8000
```

### Without Docker
```bash
# Frontend
hugo server -D

# Backend
cd cms-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Production Checklist

- [ ] Set secure `SECRET_KEY`
- [ ] Set strong `ADMIN_PASSWORD`
- [ ] Configure `GIT_TOKEN` with minimal permissions
- [ ] Add production domain to `ALLOWED_ORIGINS`
- [ ] Set `DEBUG=false`
- [ ] Enable SSL/TLS in Coolify
- [ ] Configure backup for volumes
- [ ] Setup monitoring (Coolify built-in)
- [ ] Test health check endpoints
- [ ] Verify auto-deployment on Git push

## Support

- **Hugo docs**: https://gohugo.io/documentation/
- **FastAPI docs**: https://fastapi.tiangolo.com/
- **Coolify docs**: https://coolify.io/docs/
- **Nginx docs**: https://nginx.org/en/docs/

## License

MIT License - See LICENSE file for details
