# --- Bygg (Hugo extended) ---
# Velg en HUGO_VERSION som finnes; 0.137.0 er et trygt eksempel.
ARG HUGO_VERSION=0.137.0
FROM docker.io/hugomods/hugo:exts-${HUGO_VERSION} AS build
WORKDIR /src

# Hjelper cache hvis du endrer konfig sjeldnere enn innhold
COPY hugo.toml hugo.yaml config.toml* ./ 2>/dev/null || true
COPY . .
ENV HUGO_ENV=production
RUN hugo --gc --minify

# --- Serve statiske filer med nginx ---
FROM nginx:alpine
COPY --from=build /src/public /usr/share/nginx/html
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost/ >/dev/null 2>&1 || exit 1
EXPOSE 80
