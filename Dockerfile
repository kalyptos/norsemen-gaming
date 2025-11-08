# --- Bygg (Hugo extended, pinn versjon) ---
FROM klakegg/hugo:0.134.2-ext-alpine AS build
WORKDIR /src
# Hjelper Docker cache: kopier config først
COPY hugo.toml hugo.yaml config.toml* ./ 2>/dev/null || true
COPY . .
ENV HUGO_ENV=production
RUN hugo --minify

# --- Serve statiske filer med nginx ---
FROM nginx:alpine
COPY --from=build /src/public /usr/share/nginx/html
# (Valgfritt) Healthcheck for raskere feilfanging
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost/ >/dev/null 2>&1 || exit 1
EXPOSE 80
# nginx:alpine har allerede CMD ["nginx","-g","daemon off;"]
