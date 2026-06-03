# Build stage - Frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/client

COPY client/package*.json ./

RUN npm install

COPY client .

RUN npm run build

# Build stage - Backend dependencies
FROM node:18-alpine AS backend-builder

WORKDIR /app/server

COPY server/package*.json ./

RUN npm install --production

# Final stage
FROM node:18-alpine

WORKDIR /app

# Install Python 3 and pip for GEO engine
RUN apk add --no-cache \
    python3 \
    py3-pip \
    bash \
    curl

# Copy backend dependencies
COPY --from=backend-builder /app/server/node_modules ./server/node_modules

# Copy backend source
COPY server ./server

# Copy frontend build
COPY --from=frontend-builder /app/client/dist ./public

# Copy engine
COPY engine ./engine

# Install Python dependencies
RUN pip3 install --no-cache-dir -r engine/requirements.txt

# Create .env placeholder
RUN echo "PORT=5000" > server/.env

# Expose ports
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Start server
WORKDIR /app/server

CMD ["node", "src/server.js"]
