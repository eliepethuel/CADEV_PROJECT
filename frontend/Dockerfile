# syntax=docker/dockerfile:1

# --- Dépendances -------------------------------------------------------------
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json .npmrc ./
# sharp (optimiseur d'images, lié à libvips sous LGPL) est une dépendance optionnelle de
# Next.js que l'application n'utilise pas : elle est retirée avant la construction.
RUN npm ci --no-audit --no-fund \
    && rm -rf node_modules/sharp node_modules/@img

# --- Construction ------------------------------------------------------------
FROM node:22-alpine AS build
WORKDIR /app
# L'adresse de l'API est lue par le navigateur : elle est figée à la construction.
ARG NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL} \
    NEXT_TELEMETRY_DISABLED=1
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# --- Exécution (sortie standalone, utilisateur non-root) ---------------------
FROM node:22-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000 \
    HOSTNAME=0.0.0.0
COPY --from=build --chown=node:node /app/.next/standalone ./
COPY --from=build --chown=node:node /app/.next/static ./.next/static
USER node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:3000/ >/dev/null || exit 1
CMD ["node", "server.js"]
