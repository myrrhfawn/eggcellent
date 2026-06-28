# Build context = repo root (see docker-compose: web.build.context: .)

# --- builder: build the SPA ---
FROM node:20-alpine AS builder

WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# --- runtime: nginx serves static files + proxies to the backend ---
FROM nginx:alpine AS runtime

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
