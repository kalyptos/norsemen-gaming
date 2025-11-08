# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Norsemen Gaming (norsemen.ovh) is a Hugo-based static site for Norwegian gaming content, primarily focused on space/sci-fi games. Content is written in Norwegian (language code: 'no').

## Build & Development Commands

```bash
# Local development server with drafts visible
hugo server -D

# Build for production (minified, optimized)
hugo --gc --minify

# Build with future-dated posts
hugo --gc --minify --buildFuture

# Preview build output
hugo server --source public
```

### Docker Development

```bash
# Build Docker image
docker build -t norsemen-gaming .

# Run container (serves on port 80)
docker run -p 8080:80 norsemen-gaming
```

### Content Creation

```bash
# Create new blog post (uses post archetype)
hugo new content/posts/<game-name>/<post-slug>/index.md

# Create new page (uses page archetype)
hugo new content/<page-name>.md
```

## Architecture

### Hugo Configuration
- **Hugo version**: 0.148.2 (specified in netlify.toml)
- **Requires**: Hugo Extended (for image processing with .Fit in layouts/partials/head.html)
- **Deployment**: Netlify with automatic builds
- **Output**: /public directory (git-ignored)

### Layout System

The site uses a custom layout architecture with modular components:

- **baseof.html**: Base template with Norwegian lang attribute, includes header/footer partials
- **Partials**:
  - `head.html`: SEO meta tags, Open Graph/Twitter cards, CSS bundling with SRI
  - `header.html`: Site navigation
  - `footer.html`: Footer content
  - `sidebar.html`: Sidebar widget area
  - `post-card.html`: Blog post card component
  - `pagination.html`: Pagination controls
- **Templates**:
  - `index.html`: Homepage with 9 most recent posts in grid + sidebar
  - `_default/single.html`: Individual post/page view
  - `_default/list.html`: Archive/category listing pages
  - `page/single.html`: Static page template

### CSS Architecture

The site uses a modular CSS system bundled in head.html:

1. **variables.css** - CSS custom properties for theming
2. **base.css** - Reset, typography, base element styles
3. **layout.css** - Grid systems, container, spacing
4. **components.css** - Reusable UI components
5. **blog.css** - Blog-specific styles

All CSS files are concatenated, minified, and served with SRI (Subresource Integrity) hashing via Hugo Pipes.

### Content Structure

Posts are organized using Hugo's page bundle pattern:

```
content/posts/
├── <game-name>/           # Game-specific directory
│   ├── _index.md          # Optional section page
│   └── <post-slug>/       # Individual post (page bundle)
│       ├── index.md       # Post content with frontmatter
│       └── feature.jpg    # Featured image (referenced via 'featured' param)
```

#### Post Frontmatter Structure
```yaml
title: "Post Title"
date: 2024-01-01
author: "Norsemen"
categories: []
tags: []
featured: "feature.jpg"    # Image in same directory OR assets/images/
summary: "Brief description"
draft: true                # Remove or set false to publish
```

#### Featured Image Handling
The head.html partial handles featured images with fallback logic:
1. First checks page bundle resources (same folder as index.md)
2. Falls back to assets/images/ directory
3. If Hugo Extended: generates optimized WebP (1200x630) for social media
4. If Hugo standard: uses original image

### Current Game Topics
Content covers: Spacecraft, Star Citizen, No Man's Sky, Crimson Desert, Dune Awakening, Space Engineers 2, Jump Space, Light No Fire, In the Black, Free Stars: Children of Infinity.

## Key Technical Details

### Hugo Configuration (hugo.toml)
- **baseURL**: https://norsemen.ovh
- **Permalinks**: Posts use /posts/:title/ structure (no date in URL)
- **Taxonomies**: Categories and tags enabled
- **Minification**: Enabled for production builds

### Build Optimization
- Git info injection enabled (HUGO_ENABLEGITINFO)
- Garbage collection with --gc flag
- Output minification for HTML/CSS/JS
- Resources cached in resources/_gen/ (git-ignored)

## Deployment

**Netlify** is configured as the primary deployment platform:
- Production builds on push to main branch
- Deploy previews with future-dated content for PR previews
- Environment variables set in netlify.toml
- Custom build command with minification and gc

**Docker** support available via Dockerfile:
- Two-stage build (Hugo build + Nginx serve)
- Uses klakegg/hugo:ext-alpine for builds
- Serves from /usr/share/nginx/html on port 80

## Content Management

Two CMS options available:

### Decap CMS (Recommended)
- **Location**: `/static/admin/`
- **Access**: https://norsemen.ovh/admin/
- **Features**: Git-based, no backend needed, OAuth authentication
- **Config**: `/static/admin/config.yml`

### FastAPI Backend (Custom)
- **Location**: `/cms-backend/`
- **Access**: http://localhost:8000
- **Features**: Full API, custom auth, GitHub/Gitea integration
- **Setup**: See `/cms-backend/README.md`

For full CMS documentation, see `CMS-SETUP.md`
