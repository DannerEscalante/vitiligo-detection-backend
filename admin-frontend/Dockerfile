# Etapa 1: Construcción
FROM node:18-alpine AS builder
WORKDIR /app

# Instalar dependencias
COPY package*.json ./
RUN npm ci

# Copiar el código fuente
COPY . .

# Argumento para la URL de la API (por defecto relativo /api)
ARG NEXT_PUBLIC_API_BASE_URL=/api
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL

# Compilar la aplicación Next.js
RUN npm run build

# Etapa 2: Runner de producción
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Copiar archivos esenciales desde la etapa de construcción
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000

CMD ["npm", "start"]
