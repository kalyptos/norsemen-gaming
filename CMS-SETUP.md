# Norsemen Gaming - CMS Setup Guide

This guide explains the two CMS options available for managing your blog content.

## 🚀 Quick Comparison

| Feature | Decap CMS | FastAPI Backend |
|---------|-----------|-----------------|
| **Setup Time** | 5 minutes | 15 minutes |
| **Hosting** | Static (free) | Requires server |
| **Customization** | Limited | Fully customizable |
| **Best For** | Quick start, simplicity | Custom features, control |

---

## Option 1: Decap CMS (Recommended for Quick Start)

**✅ Pros:**
- No backend server needed
- Beautiful built-in markdown editor
- Free forever (open source)
- Automatic GitHub/Gitea integration
- Live preview
- Media library

**Access:** `https://norsemen.ovh/admin/`

### Setup Steps

1. **Configure OAuth** (one-time setup):

   **For GitHub:**
   ```bash
   # Add to netlify.toml (if using Netlify):
   [build]
     command = "hugo --gc --minify"

   # Or use GitHub OAuth App:
   # 1. Go to GitHub Settings → Developer settings → OAuth Apps
   # 2. Create new OAuth App
   # 3. Homepage URL: https://norsemen.ovh
   # 4. Callback URL: https://api.netlify.com/auth/done
   # 5. Copy Client ID/Secret to Netlify settings
   ```

   **For Gitea:**
   - Create OAuth application in Gitea settings
   - Update `/static/admin/config.yml` with your Gitea URL

2. **Access the CMS:**
   - Navigate to `https://norsemen.ovh/admin/`
   - Click "Login with GitHub" (or Gitea)
   - Start creating content!

3. **Create a Post:**
   - Click "Blogginnlegg" → "Ny post"
   - Fill in the form
   - Upload images directly
   - Preview in real-time
   - Publish (commits to GitHub/Gitea)

### Configuration

File: `/static/admin/config.yml`

```yaml
backend:
  name: github  # or gitea
  repo: kalyptos/norsemen-gaming
  branch: main
```

---

## Option 2: FastAPI Backend (Custom CMS)

**✅ Pros:**
- Full control over features
- Custom authentication
- API for integrations
- Extensible for future needs

**Access:** `http://localhost:8000` (or your server URL)

### Setup Steps

1. **Install Dependencies:**
   ```bash
   cd cms-backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   ```bash
   cp .env.example .env
   nano .env  # Edit configuration
   ```

   Required settings:
   ```env
   SECRET_KEY=your-random-secret-key-here
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=your-secure-password

   # GitHub
   GITHUB_TOKEN=ghp_your_token_here
   GITHUB_REPO=kalyptos/norsemen-gaming
   GITHUB_BRANCH=main
   ```

3. **Generate GitHub Token:**
   - Go to https://github.com/settings/tokens
   - Generate new token (classic)
   - Select scopes: `repo` (full control)
   - Copy token to `.env`

4. **Run the Server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access Admin UI:**
   - Open `http://localhost:8000`
   - Login with your credentials
   - Create posts via the form

### API Usage

**Authentication:**
```bash
# Get token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=yourpassword"

# Returns: {"access_token": "...", "token_type": "bearer"}
```

**Create Post:**
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My New Post",
    "author": "Norsemen",
    "game": "star-citizen",
    "description": "This is my post description",
    "categories": ["gaming", "space"],
    "tags": ["multiplayer"],
    "featured": "feature.jpg",
    "content": "## Hello\n\nThis is my post content in markdown.",
    "draft": false
  }'
```

**Upload Image:**
```bash
curl -X POST http://localhost:8000/api/uploads/image \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/image.jpg" \
  -F "game=star-citizen"
```

### Deployment

**Docker:**
```bash
cd cms-backend
docker build -t norsemen-cms .
docker run -p 8000:8000 --env-file .env norsemen-cms
```

**Systemd Service:**
```ini
[Unit]
Description=Norsemen CMS
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/cms-backend
Environment="PATH=/path/to/cms-backend/venv/bin"
ExecStart=/path/to/cms-backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

---

## 📝 Content Workflow

### Using Decap CMS

1. Go to `/admin/`
2. Click "Blogginnlegg" → "Ny post"
3. Fill in form:
   - **Tittel**: Post title
   - **Spill/Kategori**: Select game
   - **Beskrivelse**: SEO description
   - **Innhold**: Write in markdown
   - **Hovedbilde**: Upload image
4. Click "Publish"
5. Decap commits to GitHub/Gitea
6. Netlify auto-deploys

### Using FastAPI Backend

1. Open admin UI
2. Fill in post form
3. Write content in markdown
4. Click "Publiser innlegg"
5. Backend commits to GitHub/Gitea
6. Netlify auto-deploys

---

## 🎨 Hugo Improvements Made

### 1. **Standardized Featured Images**
- All templates now use `featured` parameter
- Supports AVIF and WebP formats
- Responsive image processing
- Proper width/height attributes (prevents layout shift)

### 2. **Enhanced SEO**
- Added structured data (JSON-LD)
- Article-specific Open Graph tags
- Twitter Card optimization
- RSS feed link
- Sitemap configuration
- Robots meta tag

### 3. **Accessibility Improvements**
- Skip link for keyboard navigation
- Proper ARIA labels
- Semantic HTML landmarks
- Focus-visible styles
- Color contrast compliance

### 4. **Performance Optimizations**
- Resource hints (preload, preconnect)
- Image optimization with AVIF/WebP
- Modern CSS with logical properties
- Minification enabled
- SRI hashing for security

### 5. **New Features**
- Reading time indicator
- Related posts section
- Table of contents (for posts >500 words)
- PWA manifest
- Dark mode color scheme

---

## 🔧 Troubleshooting

### Decap CMS Issues

**"Unable to access your GitHub account"**
- Check OAuth app configuration
- Verify callback URL is correct
- Ensure you authorized the app

**"Error loading config.yml"**
- Check YAML syntax in `/static/admin/config.yml`
- Verify file is accessible at `/admin/config.yml`

### FastAPI Backend Issues

**"401 Unauthorized"**
- Check if token is still valid
- Verify `SECRET_KEY` in `.env`
- Login again to get new token

**"GitHub API error"**
- Verify token has `repo` scope
- Check repo name format: `username/repo`
- Ensure token hasn't expired

---

## 📚 Additional Resources

- **Hugo Documentation**: https://gohugo.io/documentation/
- **Decap CMS Docs**: https://decapcms.org/docs/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Netlify Docs**: https://docs.netlify.com/

---

## 🎯 Recommendation

**For most users:** Start with **Decap CMS**
- Easier setup
- No server costs
- Production-ready

**For developers:** Use **FastAPI Backend**
- Full customization
- API for automation
- Learning opportunity

---

## 🚀 Next Steps

1. Choose your CMS option
2. Follow setup instructions above
3. Create your first post
4. Customize as needed

Questions? Check the README files in each directory for more details.
