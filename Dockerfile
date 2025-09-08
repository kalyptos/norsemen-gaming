# Bygg (Hugo extended)
FROM klakegg/hugo:ext-alpine AS build
WORKDIR /src
COPY . .
RUN hugo --minify

# Serve statiske filer med nginx
FROM nginx:alpine
COPY --from=build /src/public /usr/share/nginx/html
EXPOSE 80