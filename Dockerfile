# Bygg (Hugo extended) - pinned version for reproducibility
FROM klakegg/hugo:0.148.2-ext-alpine AS build
WORKDIR /src

# Copy files in order of least to most frequently changed for better caching
COPY hugo.toml ./
COPY archetypes/ ./archetypes/
COPY layouts/ ./layouts/
COPY content/ ./content/
COPY assets/ ./assets/
COPY static/ ./static/
COPY netlify/ ./netlify/

# Build with garbage collection and minification
RUN hugo --gc --minify

# Serve statiske filer med nginx - pinned version
FROM nginx:1.25-alpine
COPY --from=build /src/public /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1
