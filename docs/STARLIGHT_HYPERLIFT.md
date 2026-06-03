# Starlight Hyperlift Deployment Guide

## Using Starlight Hyperlift Console

1. **Connect your GitHub repo**
   - Go to Starlight Hyperlift dashboard
   - Select "Connect Repository"
   - Choose your GitHub repo: `BUCS2424/a2g-one-geo-visibility-tool`

2. **Configure Build Settings**
   - **Dockerfile Path**: `Dockerfile` (in root)
   - **Build Context**: `.` (repository root)
   - **Environment Variables**: Add these in the dashboard:
     ```
     MONGODB_URI=mongodb://admin:PASSWORD@mongodb:27017/geo-visibility?authSource=admin
     JWT_SECRET=your_secure_jwt_secret_32_chars_min
     OPENAI_API_KEY=sk-your-key
     GOOGLE_API_KEY=your-key
     PORT=5000
     NODE_ENV=production
     ```

3. **Configure Services**
   - Primary container: Port 5000
   - Add MongoDB service (or use managed MongoDB)

4. **Deploy**
   - Click "Deploy"
   - Wait for Kaniko build to complete
   - Access via your Starlight domain

## Manual Deployment (if needed)

```bash
# Clone repo to your VM
git clone https://github.com/BUCS2424/a2g-one-geo-visibility-tool.git
cd a2g-one-geo-visibility-tool

# Build with Kaniko locally
kaniko --context . \
  --dockerfile ./Dockerfile \
  --destination your-registry/geo-visibility:latest \
  --cache=true \
  --no-push  # Remove if pushing to registry
```

## Environment Setup in Starlight

Add these environment variables in the Starlight console:

```
# Database
MONGODB_URI=mongodb+srv://admin:your_password@your-cluster.mongodb.net/geo-visibility?authSource=admin

# Auth
JWT_SECRET=use_a_strong_32_character_secret_key_here

# APIs
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# Server
PORT=5000
NODE_ENV=production
VITE_API_URL=https://your-domain.com
```

## Verification

After deployment:

```bash
# Check if running
curl https://your-starlight-domain/api/health

# Expected response:
# {"status":"OK","timestamp":"...","environment":"production"}
```

## Troubleshooting

### Build fails with "Dockerfile not found"
- Ensure Dockerfile is in repository root
- Build context should be `.` (dot)
- Dockerfile path should be `Dockerfile` (no leading slash)

### Application not accessible
- Check that port 5000 is exposed
- Verify environment variables are set
- Check logs in Starlight dashboard

### Database connection issues
- Verify MONGODB_URI is correct
- Check MongoDB whitelist includes your IP
- Test connection: `nc -zv your-db-host 27017`

### High memory/CPU usage
- Limit Node.js heap: `NODE_OPTIONS=--max-old-space-size=512`
- Add to environment variables in Starlight
