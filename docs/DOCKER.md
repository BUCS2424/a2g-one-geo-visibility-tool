# Docker Deployment Guide

## Prerequisites
- Docker installed on your Starlight Hyperlift VM
- Docker Compose installed
- Git installed

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/BUCS2424/a2g-one-geo-visibility-tool.git
cd a2g-one-geo-visibility-tool
```

### 2. Configure environment variables
```bash
cp .env.docker.example .env
```

Edit `.env` with your configuration:
```
MONGO_PASSWORD=your_secure_mongo_password
JWT_SECRET=your_secure_jwt_secret
OPENAI_API_KEY=sk-your-key-here
GOOGLE_API_KEY=your_google_key
```

### 3. Build and run with Docker Compose
```bash
docker-compose up --build -d
```

This will:
- Build the Docker image
- Start MongoDB container
- Start Node.js server (serving both API and frontend)
- Set up networking between services
- Run health checks

### 4. Verify deployment
```bash
# Check running containers
docker-compose ps

# View logs
docker-compose logs -f server

# Check health
curl http://localhost:5000/api/health
```

### 5. Access the application
- **Frontend**: http://your-vm-ip:3000
- **API**: http://your-vm-ip:5000/api
- **MongoDB**: localhost:27017 (internal only)

---

## Server Management

### Stop the application
```bash
docker-compose down
```

### Restart services
```bash
docker-compose restart
```

### View logs
```bash
docker-compose logs -f server    # Server logs
docker-compose logs -f mongodb   # Database logs
```

### Rebuild after code changes
```bash
docker-compose up --build -d
```

### Clean up (remove volumes)
```bash
docker-compose down -v
```

---

## Production Optimization

### 1. Update Dockerfile for production
The current Dockerfile is optimized for:
- Multi-stage builds (smaller image size)
- Alpine Linux (minimal dependencies)
- Non-root user capability

### 2. SSL/TLS with Nginx reverse proxy
Create `nginx.conf`:
```nginx
upstream backend {
    server server:5000;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/certs/cert.pem;
    ssl_certificate_key /etc/nginx/certs/key.pem;

    client_max_body_size 10M;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://backend/api/;
        proxy_set_header Authorization $http_authorization;
    }
}
```

### 3. Add Nginx to docker-compose.yml
```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/conf.d/default.conf
    - /etc/letsencrypt/live/your-domain:/etc/nginx/certs
  depends_on:
    - server
```

### 4. Database backups
```bash
# Backup MongoDB
docker-compose exec mongodb mongodump --username admin --password $MONGO_PASSWORD --authenticationDatabase admin --out /backup

# Restore from backup
docker-compose exec mongodb mongorestore --username admin --password $MONGO_PASSWORD --authenticationDatabase admin /backup
```

---

## Environment Variables for VM

### Starlight Hyperlift specific setup
```bash
# SSH into your VM
ssh root@your-vm-ip

# Clone repo
git clone https://github.com/BUCS2424/a2g-one-geo-visibility-tool.git
cd a2g-one-geo-visibility-tool

# Create .env from example
cp .env.docker.example .env

# Edit with your values
nano .env

# Start application
docker-compose up -d

# Monitor
docker-compose logs -f
```

---

## Troubleshooting

### Port already in use
```bash
# Check what's using the port
lsof -i :5000
lsof -i :3000
lsof -i :27017

# Change ports in docker-compose.yml if needed
```

### MongoDB connection issues
```bash
# Check MongoDB logs
docker-compose logs mongodb

# Test connection
docker-compose exec server nc -zv mongodb 27017
```

### Container won't start
```bash
# Check logs
docker-compose logs server

# Rebuild without cache
docker-compose build --no-cache
docker-compose up -d
```

### High memory usage
```bash
# Limit container memory in docker-compose.yml
services:
  server:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

---

## Performance Tips

1. **Use named volumes** for data persistence
2. **Enable compression** in docker-compose
3. **Set resource limits** to prevent runaway processes
4. **Use multi-stage builds** (already implemented)
5. **Enable layer caching** during builds
6. **Use .dockerignore** to reduce image size

---

## Security Best Practices

1. ✅ Use strong JWT_SECRET (32+ characters)
2. ✅ Use strong MONGO_PASSWORD
3. ✅ Keep API keys in .env (never commit to git)
4. ✅ Use SSL/TLS in production
5. ✅ Run containers as non-root user
6. ✅ Set resource limits
7. ✅ Use secrets management for sensitive data
8. ✅ Regularly update base images

---

## Monitoring & Logging

### Check container status
```bash
docker-compose ps
```

### Real-time logs
```bash
docker-compose logs -f --tail=100
```

### Check resource usage
```bash
docker stats
```

---

## Next Steps

1. Configure your domain name
2. Set up SSL certificates (Let's Encrypt)
3. Configure backups
4. Set up monitoring/alerts
5. Configure CDN for static assets
6. Set up CI/CD pipeline
