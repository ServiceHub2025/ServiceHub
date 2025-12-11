# ServiceHub Local Setup Guide

## 🎯 Person A (Backend Lead) - Initial Setup Instructions

This guide will help you set up the ServiceHub project locally and push it to your team's GitHub repository.

---

## Prerequisites

Before starting, ensure you have installed:

- ✅ **Git** (2.30+)
- ✅ **Docker** & **Docker Compose** (20.10+)
- ✅ **Node.js** (18+) & npm
- ✅ **Python** (3.11+)
- ✅ **PostgreSQL client** (psql) - for verification

---

## Step 1: Navigate to Project Directory

```bash
cd /path/to/servicehub
```

---

## Step 2: Initialize Git Repository

```bash
# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "chore: initial project setup with backend and frontend structure

- Add FastAPI backend with SQLAlchemy models
- Add React + TypeScript frontend with Vite
- Configure Docker Compose for PostgreSQL, Redis, Backend, Frontend
- Add Alembic for database migrations
- Configure TailwindCSS for styling
- Add comprehensive README with team roadmap"
```

---

## Step 3: Create GitHub Repository

1. Go to https://github.com/new
2. **Repository name**: `servicehub`
3. **Description**: "On-demand home services marketplace - Hackathon MVP"
4. **Visibility**: Private (recommended for team project)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

---

## Step 4: Link Local Repository to GitHub

```bash
# Add remote origin (replace YOUR_ORG with your GitHub username/org)
git remote add origin https://github.com/YOUR_ORG/servicehub.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main

# If main branch doesn't exist, create it
git branch -M main
git push -u origin main
```

---

## Step 5: Set Up Branch Protection Rules

1. Go to your GitHub repository
2. Click **Settings** → **Branches**
3. Click **Add branch protection rule**
4. Branch name pattern: `main`
5. Enable:
   - ✅ Require pull request before merging
   - ✅ Require approvals: 1
   - ✅ Dismiss stale pull request approvals when new commits are pushed
6. Click **Create**

---

## Step 6: Set Up Local Development Environment

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Generate a secure SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Update .env with the generated SECRET_KEY
# Edit .env file and replace SECRET_KEY value
```

### Frontend Setup

```bash
cd ../frontend

# Install Node dependencies
npm install

# Create .env file
cp .env.example .env
```

---

## Step 7: Start Services with Docker Compose

```bash
# Go back to project root
cd ..

# Start all services (PostgreSQL, Redis, Backend, Frontend)
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

**What this does:**
- 🐘 Starts PostgreSQL 15 with PostGIS extension on port 5432
- 🔴 Starts Redis 7 on port 6379
- 🐍 Starts FastAPI backend on port 8000
- ⚛️ Starts React frontend on port 5173

---

## Step 8: Verify Services are Running

### Check Docker Containers

```bash
docker ps

# You should see 4 containers running:
# - servicehub-postgres
# - servicehub-redis
# - servicehub-backend
# - servicehub-frontend
```

### Check Backend API

Open browser: http://localhost:8000

You should see:
```json
{
  "status": "ok",
  "message": "ServiceHub API is running",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### Check API Documentation

Open browser: http://localhost:8000/docs

You should see FastAPI's interactive Swagger UI.

### Check Frontend

Open browser: http://localhost:5173

You should see the ServiceHub landing page.

---

## Step 9: Run Database Migrations

```bash
# Enter backend container
docker exec -it servicehub-backend bash

# Inside container, run migrations
alembic upgrade head

# Exit container
exit
```

---

## Step 10: Verify Database Setup

```bash
# Connect to PostgreSQL
docker exec -it servicehub-postgres psql -U servicehub -d servicehub

# Inside psql, check tables
\dt

# Check PostGIS extension
SELECT PostGIS_Version();

# Exit psql
\q
```

---

## Step 11: Share Repository with Team

### Invite Team Members

1. Go to GitHub repository
2. Click **Settings** → **Collaborators**
3. Click **Add people**
4. Add teammates:
   - Person B (Backend)
   - Person C (Frontend Lead)
   - Person D (Frontend)
5. Set permission: **Write** (or **Admin** for co-leads)

### Share Repository URL

Send team members:
```
Repository: https://github.com/YOUR_ORG/servicehub
Branch structure:
- main (protected, requires PR)
- person-a-auth (your branch)
- person-b-booking
- person-c-frontend-auth
- person-d-frontend-booking
```

---

## Step 12: Create Your Feature Branch

```bash
# Create and switch to your feature branch
git checkout -b person-a-auth

# Push branch to GitHub
git push -u origin person-a-auth
```

---

## Step 13: Team Onboarding Checklist

Share this checklist with teammates:

### For All Team Members:

```bash
# 1. Clone repository
git clone https://github.com/YOUR_ORG/servicehub.git
cd servicehub

# 2. Create feature branch
git checkout -b person-X-feature-name

# 3. Copy environment files
cd backend && cp .env.example .env
cd ../frontend && cp .env.example .env

# 4. Start Docker services
docker-compose up -d

# 5. Install backend dependencies (if working on backend)
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 6. Install frontend dependencies (if working on frontend)
cd frontend
npm install

# 7. Verify services
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

---

## Common Issues & Solutions

### Issue: Docker containers won't start

**Solution:**
```bash
# Stop all containers
docker-compose down

# Remove volumes
docker-compose down -v

# Rebuild and restart
docker-compose up --build
```

### Issue: Port already in use (5432, 6379, 8000, 5173)

**Solution:**
```bash
# Check what's using the port
lsof -i :5432  # On Linux/Mac
netstat -ano | findstr :5432  # On Windows

# Kill the process or change ports in docker-compose.yml
```

### Issue: Backend can't connect to PostgreSQL

**Solution:**
```bash
# Check if PostgreSQL container is healthy
docker ps

# View backend logs
docker logs servicehub-backend

# Verify DATABASE_URL in backend .env matches docker-compose.yml
```

### Issue: Frontend can't reach backend API

**Solution:**
```bash
# Check CORS settings in backend/app/main.py
# Ensure ALLOWED_ORIGINS includes http://localhost:5173

# Check VITE_API_BASE_URL in frontend/.env
# Should be: http://localhost:8000
```

### Issue: Alembic migration fails

**Solution:**
```bash
# Check if PostGIS extension is installed
docker exec -it servicehub-postgres psql -U servicehub -d servicehub -c "CREATE EXTENSION IF NOT EXISTS postgis;"

# Reset database and re-run migrations
docker-compose down -v
docker-compose up -d
docker exec -it servicehub-backend alembic upgrade head
```

---

## Next Steps for Person A

After setup is complete:

1. ✅ **Phase 1 Tasks** (see README.md):
   - Create database migration with PostGIS
   - Build authentication system (register/login)
   - Implement JWT middleware
   - Create seed data script

2. ✅ **Create Pull Request**:
   ```bash
   git add .
   git commit -m "feat(auth): implement JWT authentication system"
   git push origin person-a-auth
   ```
   - Go to GitHub and create PR to `main`
   - Request review from Person B or C

3. ✅ **Unblock Team**:
   - Notify team when auth system is ready
   - Share Postman collection for testing endpoints

---

## Useful Commands Reference

### Docker Commands
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart a service
docker-compose restart backend

# Execute command in container
docker exec -it servicehub-backend bash
```

### Git Commands
```bash
# Create branch
git checkout -b feature-name

# Commit changes
git add .
git commit -m "type(scope): description"

# Push branch
git push origin feature-name

# Pull latest from main
git checkout main
git pull origin main
git checkout feature-name
git merge main
```

### Backend Commands
```bash
# Activate virtual environment
source venv/bin/activate

# Run FastAPI locally (outside Docker)
uvicorn app.main:app --reload --port 8000

# Create new migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Run tests
pytest
```

### Frontend Commands
```bash
# Start dev server locally (outside Docker)
npm run dev

# Build for production
npm run build

# Lint code
npm run lint
```

---

## Support

If you encounter issues:

1. Check **Common Issues** section above
2. Review logs: `docker-compose logs -f`
3. Ask in team Slack channel: `#servicehub-dev`
4. Create GitHub issue with label `setup-issue`

---

## Success Checklist ✅

Before considering setup complete, verify:

- [ ] GitHub repository created and accessible to all team members
- [ ] All 4 Docker containers running successfully
- [ ] Backend API responding at http://localhost:8000
- [ ] Frontend displaying at http://localhost:5173
- [ ] API documentation accessible at http://localhost:8000/docs
- [ ] PostgreSQL accepting connections
- [ ] PostGIS extension installed
- [ ] Team members invited to repository
- [ ] Branch protection rules configured
- [ ] `.env` files created from examples
- [ ] All teammates can clone and run the project

---

**You're all set! Time to start building! 🚀**

*Last updated: December 10, 2025*
