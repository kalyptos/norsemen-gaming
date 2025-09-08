# Bygg
FROM klakegg/hugo:0.128.0-ext-alpine AS build
WORKDIR /src
COPY . .
RUN hugo --minify

# Serve
FROM nginx:alpine
COPY --from=build /src/public /usr/share/nginx/html
