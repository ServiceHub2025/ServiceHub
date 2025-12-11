# ServiceHub Quick Reference Guide

## 🚀 Quick Start (All Team Members)

### 1. Clone & Setup (First Time Only)

```bash
# Clone repository
git clone https://github.com/YOUR_ORG/servicehub.git
cd servicehub

# Create your feature branch
git checkout -b person-X-your-feature

# Setup environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start all services
docker-compose up -d
```

### 2. Daily Development

```bash
# Start Docker services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Access Points

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173
- **PostgreSQL**: localhost:5432 (user: servicehub, password: servicehub_password)
- **Redis**: localhost:6379

---

## 👥 Team Member Quick Access

### Person A (Backend Lead)

**Your Branch**: `person-a-auth`

**Primary Tasks**:
- Database schema & migrations
- Authentication system (register/login)
- JWT middleware
- Seed data script

**Key Files**:
```
backend/
  app/
    models.py          # Database models
    database.py        # DB connection
    auth/
      routes.py        # Auth endpoints
      utils.py         # JWT & password hashing
  alembic/versions/    # Migrations
  scripts/seed_data.py # Test data
```

**Commands**:
```bash
# Create migration
docker exec -it servicehub-backend alembic revision --autogenerate -m "description"

# Run migrations
docker exec -it servicehub-backend alembic upgrade head

# Access backend container
docker exec -it servicehub-backend bash
```

---

### Person B (Backend)

**Your Branch**: `person-b-booking`

**Primary Tasks**:
- Provider search with PostGIS
- Booking creation & state machine
- Review system
- Provider registration

**Key Files**:
```
backend/
  app/
    providers/
      routes.py        # Provider endpoints
      services.py      # Business logic
    bookings/
      routes.py        # Booking endpoints
      services.py      # State machine
    reviews/
      routes.py        # Review endpoints
```

**Dependencies**: Wait for Person A's auth system

---

### Person C (Frontend Lead)

**Your Branch**: `person-c-frontend-auth`

**Primary Tasks**:
- React + TypeScript setup
- AuthContext
- Login/Register pages
- Protected routes
- Axios client with JWT

**Key Files**:
```
frontend/
  src/
    contexts/AuthContext.tsx
    api/client.ts
    pages/
      LoginPage.tsx
      RegisterPage.tsx
    components/
      ProtectedRoute.tsx
      Navbar.tsx
```

**Commands**:
```bash
# Install dependencies
cd frontend && npm install

# Start dev server (outside Docker)
npm run dev

# Build for production
npm run build
```

**Dependencies**: Wait for Person A's auth API

---

### Person D (Frontend)

**Your Branch**: `person-d-frontend-booking`

**Primary Tasks**:
- Provider search UI
- Booking form
- My Bookings page
- Review submission

**Key Files**:
```
frontend/
  src/
    pages/
      ProviderSearchPage.tsx
      BookingPage.tsx
      MyBookingsPage.tsx
    components/
      ProviderCard.tsx
      BookingCard.tsx
```

**Dependencies**: Wait for Person C's AuthContext

---

## 📝 Common Commands

### Docker

```bash
# Start all services
docker-compose up -d

# Start with rebuild
docker-compose up --build -d

# Stop services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v

# View logs
docker-compose logs -f [service-name]

# Restart specific service
docker-compose restart backend

# Execute command in container
docker exec -it servicehub-backend bash
```

### Git

```bash
# Daily sync
git checkout main && git pull origin main
git checkout YOUR_BRANCH && git merge main

# Commit changes
git add .
git commit -m "feat(scope): description"
git push origin YOUR_BRANCH

# Create PR
# Go to GitHub, click "Compare & pull request"
```

### Backend (Python)

```bash
# Activate virtual environment (local dev)
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI locally
uvicorn app.main:app --reload --port 8000

# Run tests
pytest

# Alembic commands (inside Docker or with venv)
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1
```

### Frontend (Node)

```bash
# Install dependencies
cd frontend
npm install

# Start dev server
npm run dev

# Build
npm run build

# Lint
npm run lint
```

---

## 🔍 Debugging

### Check Service Status

```bash
docker ps

# All 4 should be running:
# servicehub-postgres
# servicehub-redis
# servicehub-backend
# servicehub-frontend
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Test Database Connection

```bash
# Connect to PostgreSQL
docker exec -it servicehub-postgres psql -U servicehub -d servicehub

# Inside psql:
\dt                    # List tables
\d table_name          # Describe table
SELECT * FROM users;   # Query data
\q                     # Exit
```

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Register user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123","role":"customer","name":"Test User","phone":"1234567890"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'
```

---

## 🐛 Common Issues

### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Kill process or change port in docker-compose.yml
```

### Database Connection Failed

```bash
# Restart PostgreSQL
docker-compose restart postgres

# Check logs
docker-compose logs postgres

# Recreate database
docker-compose down -v
docker-compose up -d
```

### Frontend Can't Reach Backend

```bash
# Check CORS in backend/app/main.py
# Verify VITE_API_BASE_URL in frontend/.env
# Should be: http://localhost:8000
```

### Module Not Found (Python)

```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt

# Or rebuild Docker image
docker-compose up --build backend
```

### Module Not Found (Node)

```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install

# Or rebuild Docker image
docker-compose up --build frontend
```

---

## 📊 Project Structure Summary

```
servicehub/
├── backend/              # FastAPI Python backend
│   ├── app/
│   │   ├── auth/        # Person A
│   │   ├── providers/   # Person B
│   │   ├── bookings/    # Person B
│   │   ├── reviews/     # Person B
│   │   └── admin/       # Person A
│   ├── alembic/         # Database migrations
│   └── tests/           # Backend tests
│
├── frontend/            # React TypeScript frontend
│   └── src/
│       ├── contexts/    # Person C
│       ├── pages/       # Person C & D
│       ├── components/  # Person C & D
│       └── api/         # Person C
│
├── docs/                # Documentation
├── docker-compose.yml   # Docker orchestration
└── README.md            # Main documentation
```

---

## 🎯 Success Checklist

Before considering a task complete:

### Backend Tasks
- [ ] Code follows Python conventions (PEP 8)
- [ ] Endpoint tested with Postman/curl
- [ ] Error handling implemented
- [ ] Docstrings added
- [ ] No console errors

### Frontend Tasks
- [ ] Code follows TypeScript conventions
- [ ] Component tested in browser
- [ ] Responsive design (mobile-friendly)
- [ ] No console errors
- [ ] Loading states implemented

### Both
- [ ] Committed with meaningful message
- [ ] Pushed to feature branch
- [ ] PR created with description
- [ ] Reviewer assigned
- [ ] CI checks pass

---

## 📞 Getting Help

1. **Check documentation**: README.md, SETUP_GUIDE.md, GIT_WORKFLOW.md
2. **Review logs**: `docker-compose logs -f`
3. **Ask in Slack**: #servicehub-dev
4. **Create GitHub issue**: Tag with `question` or `help-wanted`
5. **Ping teammates**: @Person-A for backend, @Person-C for frontend

---

## 🎉 Demo Day Checklist

Final checks before demo:

- [ ] All Docker services running
- [ ] Database seeded with demo data
- [ ] Demo user accounts created
- [ ] End-to-end flow tested
- [ ] No console errors
- [ ] Presentation slides ready
- [ ] GitHub repo cleaned up
- [ ] README updated with screenshots

---

**You got this! Let's build something amazing! 🚀**

*Last updated: December 10, 2025*
