# --- Bygg (Hugo extended) ---
FROM docker.io/hugomods/hugo:exts-0.137.0 AS build
WORKDIR /src
COPY . .
ENV HUGO_ENV=production
RUN hugo --gc --minify

# --- Serve statiske filer med nginx ---
FROM nginx:alpine
COPY --from=build /src/public /usr/share/nginx/html
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost/ >/dev/null 2>&1 || exit 1
EXPOSE 80
