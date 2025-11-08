# ============================================
# Norsemen Gaming - Production Dockerfile
# ============================================
# Stage 1: Build Hugo Site
FROM klakegg/hugo:0.148.2-ext-alpine AS build

WORKDIR /src

# Copy source files
COPY . .

# Build production site
RUN hugo --gc --minify --buildFuture

# Verify build
RUN ls -la /src/public

# ============================================
# Stage 2: Production Web Server
FROM nginx:1.25-alpine

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy custom nginx config
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Copy built site from build stage
COPY --from=build /src/public /usr/share/nginx/html

# Create nginx cache directories
RUN mkdir -p /var/cache/nginx/client_temp \
    && mkdir -p /var/cache/nginx/proxy_temp \
    && mkdir -p /var/cache/nginx/fastcgi_temp \
    && mkdir -p /var/cache/nginx/uwsgi_temp \
    && mkdir -p /var/cache/nginx/scgi_temp \
    && chown -R nginx:nginx /var/cache/nginx \
    && chown -R nginx:nginx /usr/share/nginx/html \
    && chmod -R 755 /usr/share/nginx/html

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Expose port 80
EXPOSE 80

# Use non-root user
USER nginx

# Start nginx
CMD ["nginx", "-g", "daemon off;"]