# ServiceHub - On-Demand Home Services Platform

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-MVP-orange.svg)

> A modern, scalable on-demand home services marketplace connecting customers with verified service providers. Built for hackathons with production-ready architecture.

---

## 📋 Table of Contents

- [Executive Summary](#executive-summary)
- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Team Organization](#team-organization)
- [Development Roadmap](#development-roadmap)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Setup Instructions](#setup-instructions)
- [Development Workflow](#development-workflow)
- [Success Metrics](#success-metrics)
- [MVP Scope](#mvp-scope)

---

## 🎯 Executive Summary

ServiceHub is a modern, scalable on-demand home services marketplace that connects customers with verified service providers for cleaning, plumbing, electrical, and interior design services. Built with a microservices-oriented architecture, the platform enables:

- **Transparent pricing** with automatic calculation (Base Price × Quantity × 1.15 commission)
- **Real-time availability** management with booking confirmations
- **Location-based search** within configurable radius (5km/10km/20km)
- **Bidirectional rating system** for quality assurance
- **Streamlined booking** with <3 minute booking flow

**MVP Timeline**: 20-24 hours with 4-person team  
**Target**: Functional demo with end-to-end booking flow

---

## 🔴 Problem Statement

Current challenges in the home services market:

- ❌ **Lack of transparency** in pricing and provider credentials
- ❌ **Difficulty finding providers** during urgent needs
- ❌ **No centralized platform** for quality assurance and reviews
- ❌ **Complex booking processes** requiring multiple phone calls
- ❌ **Limited accountability** for both customers and providers

---

## ✅ Solution Overview

ServiceHub addresses these challenges through:

1. **Transparent Upfront Pricing**
   - Automatic calculation: `Total = (Base Price × Quantity) × 1.15`
   - Example: Cleaning 3 rooms at $30/room = $103.50

2. **Real-time Provider Search**
   - PostGIS-powered geospatial queries
   - Distance-based filtering within radius
   - Sort by rating and proximity

3. **Quality Assurance**
   - Bidirectional rating system (customers ↔ providers)
   - Average rating calculation: `AVG(all_ratings)`
   - Minimum 3 reviews required for public display

4. **Instant Booking**
   - State machine: `REQUESTED → ACCEPTED → IN_PROGRESS → COMPLETED`
   - Overlap validation prevents double-booking
   - Business hours enforcement (8 AM - 8 PM)

5. **Provider Verification**
   - Admin approval workflow before going live
   - Document verification (out of scope for MVP)

---

## 🛠 Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 18 + TypeScript | Type-safe UI development |
| **Styling** | TailwindCSS 3+ | Utility-first CSS framework |
| **Backend** | FastAPI (Python 3.11+) | High-performance async API |
| **Database** | PostgreSQL 15+ | Primary data store |
| **Geolocation** | PostGIS extension | Spatial queries & distance calculation |
| **Cache** | Redis 7+ | Session management & availability cache |
| **Authentication** | JWT + bcrypt | Secure token-based auth |
| **Real-time** | WebSockets (optional) | Live booking notifications |
| **Deployment** | Docker + Docker Compose | Containerized development |

**Why this stack?**
- **FastAPI**: Native async support, automatic OpenAPI docs, fastest Python framework
- **PostgreSQL + PostGIS**: Industry-standard for geospatial data
- **React + TypeScript**: Type safety prevents runtime errors
- **Docker**: Consistent dev/prod environments

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Layer                              │
│  React 18 + TypeScript + TailwindCSS (Port 5173)           │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP/REST + WebSocket
                   │ JWT Bearer Token
┌──────────────────▼──────────────────────────────────────────┐
│                  API Gateway (FastAPI)                       │
│  Authentication Middleware | CORS | Rate Limiting           │
└─────┬────────────┬────────────┬────────────┬────────────────┘
      │            │            │            │
      ▼            ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│   Auth   │ │ Provider │ │ Booking  │ │  Review  │
│  Module  │ │  Module  │ │  Module  │ │  Module  │
└────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │            │
     └────────────┴────────────┴────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│            Database Layer (PostgreSQL + PostGIS)             │
│  users | services | service_providers | bookings | reviews  │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
servicehub/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── config.py                  # Environment config (DB, JWT)
│   │   ├── database.py                # SQLAlchemy engine & session
│   │   ├── models.py                  # ORM models (User, Booking, etc.)
│   │   ├── schemas.py                 # Pydantic request/response models
│   │   │
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py              # POST /auth/register, /auth/login
│   │   │   ├── utils.py               # JWT creation, password hashing
│   │   │   └── dependencies.py        # get_current_user, require_role
│   │   │
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py              # GET /providers/search, POST /providers/register
│   │   │   └── services.py            # Business logic (distance calc)
│   │   │
│   │   ├── bookings/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py              # POST /bookings, PATCH /bookings/:id/status
│   │   │   ├── services.py            # State machine, overlap validation
│   │   │   └── validators.py          # Business rule checks
│   │   │
│   │   ├── reviews/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py              # POST /reviews
│   │   │   └── services.py            # Rating average calculation
│   │   │
│   │   └── admin/
│   │       ├── __init__.py
│   │       └── routes.py              # PATCH /admin/providers/:id/verify
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   │   └── 001_initial_schema.py  # Database migration
│   │   ├── env.py
│   │   └── alembic.ini
│   │
│   ├── scripts/
│   │   └── seed_data.py               # Populate DB with test data
│   │
│   ├── tests/
│   │   ├── conftest.py                # Pytest fixtures
│   │   ├── test_auth.py
│   │   ├── test_providers.py
│   │   ├── test_bookings.py
│   │   └── test_reviews.py
│   │
│   ├── requirements.txt               # Python dependencies
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts              # Axios instance + JWT interceptor
│   │   │
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx        # Global auth state (login/logout)
│   │   │
│   │   ├── components/
│   │   │   ├── Navbar.tsx             # Navigation with role-based menu
│   │   │   ├── ProtectedRoute.tsx     # Route guard for auth
│   │   │   ├── ProviderCard.tsx       # Display provider in search results
│   │   │   ├── BookingCard.tsx        # Booking list item
│   │   │   ├── StarRating.tsx         # 5-star rating display
│   │   │   └── LoadingSpinner.tsx
│   │   │
│   │   ├── pages/
│   │   │   ├── LoginPage.tsx          # Email/password login form
│   │   │   ├── RegisterPage.tsx       # User registration (role selection)
│   │   │   ├── DashboardPage.tsx      # Role-based landing page
│   │   │   ├── ProviderSearchPage.tsx # Search with filters (service/location/radius)
│   │   │   ├── BookingPage.tsx        # Booking form (date/time/hours)
│   │   │   ├── MyBookingsPage.tsx     # View booking history
│   │   │   ├── ReviewPage.tsx         # Submit review after completion
│   │   │   └── AdminDashboard.tsx     # Provider verification UI
│   │   │
│   │   ├── types/
│   │   │   └── index.ts               # TypeScript interfaces (User, Booking, etc.)
│   │   │
│   │   ├── utils/
│   │   │   ├── formatters.ts          # Date/currency formatting
│   │   │   └── validators.ts          # Client-side validation
│   │   │
│   │   ├── App.tsx                    # Root component with routing
│   │   ├── main.tsx                   # React entry point
│   │   └── index.css                  # Global styles
│   │
│   ├── public/
│   │   └── favicon.ico
│   │
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── docker-compose.yml                 # PostgreSQL + Redis + Backend + Frontend
├── .gitignore
├── README.md
└── docs/
    ├── API_CONTRACT.yaml              # OpenAPI 3.0 specification
    ├── ARCHITECTURE.md                # System design document
    └── DEVELOPMENT_GUIDE.md           # Setup & contribution guide
```

---

## 👥 Team Organization

### **4-Person Team Structure**

| Person | Role | Primary Responsibilities | Critical Path |
|--------|------|--------------------------|---------------|
| **Person A** | Backend Lead | Database schema, Auth system, Docker setup | ⚠️ BLOCKER: Everything depends on this |
| **Person B** | Backend | Booking logic, Provider search, Reviews | Depends on Person A |
| **Person C** | Frontend Lead | React setup, Auth UI, Routing | Depends on Person A |
| **Person D** | Frontend | Provider search UI, Booking flow | Depends on Person C |

---

### **Person A: Backend Lead** 🔵

**Owner**: Database, Authentication, Infrastructure

**Deliverables**:
- ✅ PostgreSQL + PostGIS Docker setup
- ✅ Complete database schema with Alembic migrations
- ✅ User authentication system (register/login)
- ✅ JWT middleware and role-based access control
- ✅ Seed data script (5 providers, 3 customers, 1 admin)

**Technologies**: FastAPI, SQLAlchemy, Alembic, PostgreSQL, PostGIS, Docker

**Key Files**:
- `docker-compose.yml`
- `backend/alembic/versions/001_initial_schema.py`
- `backend/app/auth/*`
- `backend/app/models.py`

---

### **Person B: Backend** 🟢

**Owner**: Core Business Logic

**Deliverables**:
- ✅ Provider search with PostGIS distance calculation
- ✅ Booking creation with price calculation & overlap validation
- ✅ Booking state machine (5 states, 7 valid transitions)
- ✅ Review system with automatic provider rating updates
- ✅ Provider registration endpoint

**Technologies**: FastAPI, SQLAlchemy, PostGIS

**Key Files**:
- `backend/app/providers/*`
- `backend/app/bookings/*`
- `backend/app/reviews/*`

**Dependencies**: Requires Person A's auth system (JWT, User model)

---

### **Person C: Frontend Lead** 🟡

**Owner**: React Architecture, Authentication Flow

**Deliverables**:
- ✅ Vite + React + TypeScript boilerplate
- ✅ TailwindCSS configuration
- ✅ AuthContext (login/logout/register state)
- ✅ Axios client with JWT bearer token interceptor
- ✅ Login & Registration pages
- ✅ ProtectedRoute component
- ✅ Navbar with role-based menu

**Technologies**: React 18, TypeScript, TailwindCSS, React Router, Axios

**Key Files**:
- `frontend/src/contexts/AuthContext.tsx`
- `frontend/src/api/client.ts`
- `frontend/src/pages/LoginPage.tsx`
- `frontend/src/pages/RegisterPage.tsx`

**Dependencies**: Requires Person A's auth API endpoints

---

### **Person D: Frontend** 🟠

**Owner**: Customer-Facing Features

**Deliverables**:
- ✅ Provider search page (filters: service, location, radius)
- ✅ ProviderCard component (distance, rating, price display)
- ✅ Booking form with date/time picker
- ✅ Real-time price calculation display
- ✅ My Bookings page with status tracking
- ✅ Review submission form

**Technologies**: React 18, TypeScript, TailwindCSS

**Key Files**:
- `frontend/src/pages/ProviderSearchPage.tsx`
- `frontend/src/pages/BookingPage.tsx`
- `frontend/src/pages/MyBookingsPage.tsx`
- `frontend/src/components/ProviderCard.tsx`

**Dependencies**: Requires Person C's AuthContext, Person B's APIs

---

## 🗓 Development Roadmap

### **Timeline Overview (20-24 hours)**

| Phase | Duration | Team Activity | Goal |
|-------|----------|---------------|------|
| **Phase 0** | 1 hour | All 4 together | API contract agreement |
| **Phase 1** | 6-8 hours | Parallel work | Foundation (DB + Auth + React setup) |
| **Phase 2** | 8-10 hours | Parallel work | Core features (Booking + Search) |
| **Phase 3** | 4-6 hours | Parallel work | Polish (Reviews + Admin + UI) |
| **Phase 4** | 2-4 hours | All 4 together | Testing + Demo prep |

---

### **Phase 0: API Contract (ALL 4 - 1 hour)**

**Goal**: Agree on API structure before any coding

**Activities**:
1. **Review OpenAPI specification** (`docs/API_CONTRACT.yaml`)
2. **Agree on response formats**:
   - Success: `200 OK` with data
   - Client error: `400 Bad Request` with `{error: string}`
   - Auth error: `401 Unauthorized` with `{error: "Invalid token"}`
   - Not found: `404 Not Found` with `{error: "Resource not found"}`
3. **Define TypeScript interfaces** (Person C creates `frontend/src/types/index.ts`)
4. **Set up Git workflow**:
   - Main branch protection (no direct pushes)
   - Feature branches: `person-a-auth`, `person-b-booking`, etc.
   - PR approval required from at least 1 teammate

**Deliverable**: ✅ Signed-off `API_CONTRACT.yaml` in repo

---

### **Phase 1: Foundation (Hours 1-8)**

**Goal**: Build the critical infrastructure that unblocks everyone

#### **Person A Tasks** (6-8 hours)
1. ✅ Docker Compose setup (PostgreSQL + Redis + Backend)
2. ✅ Database schema with PostGIS extension
3. ✅ Alembic migration script
4. ✅ User model with role enum (customer/provider/admin)
5. ✅ JWT authentication endpoints (`/auth/register`, `/auth/login`)
6. ✅ Auth middleware (`get_current_user`, `require_role`)
7. ✅ Seed data script with Newark, NJ coordinates

**Checkpoint**: Backend running on `localhost:8000`, Postman tests pass

#### **Person B Tasks** (6-8 hours)
*Blocked until Person A completes auth*
1. ✅ Provider search endpoint with PostGIS
2. ✅ Booking creation endpoint with price calculation
3. ✅ Booking overlap validation logic
4. ✅ Provider registration endpoint

**Checkpoint**: Can create booking via Postman, no overlaps allowed

#### **Person C Tasks** (6-8 hours)
*Blocked until Person A deploys auth API*
1. ✅ Vite + React + TypeScript project init
2. ✅ TailwindCSS + PostCSS config
3. ✅ AuthContext with login/register/logout
4. ✅ Axios client with JWT interceptor
5. ✅ Login page with form validation
6. ✅ Registration page with role selection
7. ✅ ProtectedRoute component

**Checkpoint**: Can login/register via UI, token stored in localStorage

#### **Person D Tasks** (6-8 hours)
*Blocked until Person C finishes AuthContext*
1. ✅ Navbar component with conditional rendering
2. ✅ Dashboard page (different views per role)
3. ✅ Basic provider search form
4. ✅ API integration setup

**Checkpoint**: Can navigate between pages, auth state persists

---

### **Integration Checkpoint 1 (Hour 8)**

**All 4 meet for 30 minutes**

**Test end-to-end flow**:
1. Person D registers a customer via UI
2. Token appears in Network tab (DevTools)
3. Person A verifies user in PostgreSQL
4. Person C confirms AuthContext state updates
5. Person B tests provider search via Postman

**Fix any blockers before continuing**

---

### **Phase 2: Core Features (Hours 9-16)**

**Goal**: Build the demo-worthy booking flow

#### **Person A Tasks** (3-4 hours)
1. ✅ Admin endpoints for provider verification
2. ✅ GET `/admin/providers/pending`
3. ✅ PATCH `/admin/providers/:id/verify`
4. ✅ Add CORS configuration for frontend

#### **Person B Tasks** (6-8 hours)
1. ✅ Booking state machine implementation
   - Valid transitions: `REQUESTED → ACCEPTED → IN_PROGRESS → COMPLETED`
   - Invalid transitions return `400`
2. ✅ PATCH `/bookings/:id/status` with role validation
3. ✅ GET `/bookings/me` (customer vs provider views)
4. ✅ Review submission endpoint
5. ✅ Automatic provider rating update on new review

#### **Person C Tasks** (4-6 hours)
1. ✅ Admin dashboard for provider verification
2. ✅ Pending providers table
3. ✅ Approve/Reject buttons
4. ✅ Toast notifications for success/error

#### **Person D Tasks** (6-8 hours)
1. ✅ Provider search page with filters
   - Service dropdown (fetch from `/services`)
   - Location input (browser geolocation or manual)
   - Radius selector (5km / 10km / 20km)
2. ✅ ProviderCard component
   - Display: name, rating, distance, hourly rate
   - "Book Now" button
3. ✅ Booking form page
   - Date picker (only future dates)
   - Time picker (8 AM - 8 PM, 30min intervals)
   - Hours slider (1-8 hours)
   - Real-time price calculation: `(hourly_rate × hours × 1.15)`
4. ✅ My Bookings page
   - Fetch GET `/bookings/me`
   - Display bookings table with status badges
   - "Cancel" button (if status = REQUESTED)

---

### **Integration Checkpoint 2 (Hour 16)**

**All 4 meet for 30 minutes**

**Test complete booking flow**:
1. Customer searches for plumbers in Newark within 10km
2. Selects provider, navigates to booking page
3. Chooses tomorrow 2 PM, 3 hours
4. Confirms booking (price = $50 × 3 × 1.15 = $172.50)
5. Provider logs in, accepts booking
6. Provider marks as completed
7. Customer submits 5-star review

**Fix critical bugs, defer minor issues**

---

### **Phase 3: Polish (Hours 17-20)**

**Goal**: Make it demo-ready

#### **All Team Members** (4 hours)

**Polish tasks** (split by priority):
1. ✅ Review submission UI (Person D)
2. ✅ StarRating component (Person D)
3. ✅ Loading spinners on all API calls (Person C & D)
4. ✅ Error toast notifications (Person C)
5. ✅ Responsive design fixes (Person D)
6. ✅ Provider availability check (Person B - if time permits)
7. ✅ Unit tests for critical paths (Person A & B)

**Documentation**:
- Update README with setup instructions
- Add API documentation screenshots
- Record demo video walkthrough

---

### **Phase 4: Testing & Demo Prep (Hours 21-24)**

**Goal**: Bug-free demo with compelling narrative

#### **All 4 Together** (3-4 hours)

**Testing checklist**:
- [ ] Happy path: Customer books → Provider accepts → Completes → Review
- [ ] Edge case: Overlapping bookings rejected
- [ ] Edge case: Invalid time (before 8 AM) rejected
- [ ] Edge case: Unverified provider not in search results
- [ ] Edge case: Customer cannot accept their own booking
- [ ] UI: All buttons have hover states
- [ ] UI: Mobile responsive (test on 375px width)

**Demo preparation**:
1. Create demo accounts:
   - Customer: `demo@customer.com` / `password123`
   - Provider: `demo@provider.com` / `password123`
   - Admin: `admin@servicehub.com` / `admin123`
2. Seed realistic data:
   - 5 providers with different ratings (3.5 - 5.0)
   - 3 completed bookings with reviews
   - 2 pending bookings
3. Prepare demo script:
   - Problem statement (30 sec)
   - Solution overview (1 min)
   - Live demo (3 min): Search → Book → Accept → Review
   - Architecture diagram (1 min)
   - Q&A (remainder)

**Final deliverables**:
- [ ] GitHub repo cleaned up (remove unused files)
- [ ] README with setup instructions
- [ ] Docker Compose one-command startup
- [ ] Demo video (backup if live demo fails)
- [ ] Presentation slides (10 slides max)

---

## 💾 Database Schema

### **Users Table**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('customer', 'provider', 'admin')),
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Services Table**
```sql
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    base_price DECIMAL(10, 2) NOT NULL,
    active BOOLEAN DEFAULT true
);
```

### **Service Providers Table**
```sql
CREATE TABLE service_providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    service_id INT REFERENCES services(id),
    hourly_rate DECIMAL(10, 2) NOT NULL,
    location GEOGRAPHY(POINT, 4326) NOT NULL,  -- PostGIS
    verified BOOLEAN DEFAULT false,
    rating DECIMAL(3, 2) DEFAULT 0.0 CHECK (rating >= 0 AND rating <= 5)
);

-- Critical index for distance queries
CREATE INDEX idx_provider_location ON service_providers USING GIST(location);
```

### **Bookings Table**
```sql
CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES users(id),
    provider_id UUID REFERENCES service_providers(id),
    service_id INT REFERENCES services(id),
    status VARCHAR(20) CHECK (status IN ('REQUESTED', 'ACCEPTED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
    scheduled_time TIMESTAMP NOT NULL,
    hours INT CHECK (hours >= 1 AND hours <= 8),
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_bookings_customer ON bookings(customer_id);
CREATE INDEX idx_bookings_provider ON bookings(provider_id);
CREATE INDEX idx_bookings_status ON bookings(status);
```

### **Reviews Table**
```sql
CREATE TABLE reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID REFERENCES bookings(id) UNIQUE,  -- One review per booking
    reviewer_id UUID REFERENCES users(id),
    reviewee_id UUID REFERENCES users(id),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Relationships**
- `users` 1:N `service_providers` (one user can be multiple providers)
- `service_providers` M:N `services` (providers offer multiple services)
- `bookings` M:1 `users` (customer)
- `bookings` M:1 `service_providers`
- `reviews` 1:1 `bookings` (one review per booking)

---

## 🔌 API Endpoints

### **Authentication**
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | None | Create new account (customer/provider/admin) |
| POST | `/auth/login` | None | Login and receive JWT token |

### **Services**
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/services` | None | List all active services |

### **Providers**
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/providers/search` | Optional | Search providers by location, service, radius |
| POST | `/providers/register` | Required (User) | Register as a provider |
| GET | `/providers/me` | Required (Provider) | Get provider dashboard data |

### **Bookings**
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/bookings` | Required (Customer) | Create new booking |
| GET | `/bookings/me` | Required | Get user's bookings (customer or provider view) |
| PATCH | `/bookings/:id/status` | Required | Update booking status (state machine) |
| DELETE | `/bookings/:id` | Required (Customer) | Cancel booking (only if REQUESTED) |

### **Reviews**
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/reviews` | Required (Customer) | Submit review after completed booking |

### **Admin**
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/admin/providers/pending` | Required (Admin) | List unverified providers |
| PATCH | `/admin/providers/:id/verify` | Required (Admin) | Approve/reject provider |

---

## 🚀 Setup Instructions

### **Prerequisites**
- Docker & Docker Compose (20.10+)
- Node.js (18+) & npm (for frontend development)
- Python 3.11+ (for backend development)
- Git

### **Quick Start (Entire Stack)**

```bash
# Clone repository
git clone https://github.com/your-org/servicehub.git
cd servicehub

# Start all services (PostgreSQL + Redis + Backend + Frontend)
docker-compose up --build

# Backend API: http://localhost:8000
# Frontend UI: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

### **Backend Setup (Local Development)**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
alembic upgrade head

# Seed database with test data
python scripts/seed_data.py

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Frontend Setup (Local Development)**

```bash
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev

# Frontend will be available at http://localhost:5173
```

### **Environment Variables**

**Backend (`.env`)**:
```env
# Database
DATABASE_URL=postgresql://servicehub:password@localhost:5432/servicehub

# JWT
SECRET_KEY=your-256-bit-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Frontend (`.env`)**:
```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 🔄 Development Workflow

### **Git Branching Strategy**

```
main (protected)
├── person-a-auth
├── person-b-booking
├── person-c-frontend-auth
└── person-d-frontend-booking
```

### **Branch Naming Convention**
- Feature: `person-{letter}-{feature-name}`
- Bugfix: `bugfix-{description}`
- Hotfix: `hotfix-{description}`

### **Commit Message Format**
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
```
feat(auth): add JWT token generation
fix(booking): prevent overlapping bookings
docs(readme): update setup instructions
```

### **Pull Request Process**

1. **Create PR** from feature branch to `main`
2. **Assign reviewer** (at least 1 teammate)
3. **Run tests**: `pytest` (backend), `npm test` (frontend)
4. **Check CI/CD**: All checks must pass
5. **Merge** after approval

### **Daily Standup (15 min at hours 0, 8, 16)**

**Format**:
- What I completed since last standup
- What I'm working on next
- Any blockers

**Example**:
```
Person A:
✅ Completed: Database schema, auth endpoints
🚧 Working on: Admin verification endpoints
⚠️ Blocker: None

Person B:
✅ Completed: Waiting for auth system
🚧 Working on: Provider search query
⚠️ Blocker: Need auth middleware from Person A
```

---

## 📊 Success Metrics

### **MVP Evaluation Criteria**

| Metric | Target | Measurement |
|--------|--------|-------------|
| **User Registration Success Rate** | > 95% | (Successful registrations / Total attempts) × 100 |
| **Booking Completion Time** | < 3 minutes | Time from search to booking confirmation |
| **Search Result Accuracy** | 100% | All providers within specified radius |
| **API Response Time (p95)** | < 200ms | 95th percentile latency for all endpoints |
| **System Uptime** | 99% | During 4-hour demo period |

### **Demo Success Criteria**

- [ ] Complete booking flow works end-to-end
- [ ] Geospatial search returns correct providers
- [ ] Price calculation is accurate (shows 15% commission)
- [ ] Provider cannot be double-booked
- [ ] Rating updates correctly after review submission
- [ ] UI is responsive on mobile (tested at 375px)
- [ ] No console errors in browser DevTools
- [ ] Docker Compose starts all services successfully

---

## 📦 MVP Scope

### **✅ In Scope for MVP**

- **Services**: 4 types only (Cleaning, Plumbing, Electrician, Interior Design)
- **Booking**: Single provider per booking (no team functionality)
- **Payment**: Mock tracking only (no real gateway integration)
- **Search**: Distance-based within radius (5km/10km/20km)
- **Rating**: Simple average calculation
- **Notifications**: Email via console logs (no real SMTP)
- **Authentication**: JWT-based with bcrypt password hashing

### **❌ Out of Scope for MVP**

- Team booking functionality (multiple providers per job)
- Real payment gateway (Stripe/Razorpay)
- Advanced recommendation algorithms (ML-based)
- Mobile applications (iOS/Android native)
- SMS notifications (Twilio integration)
- Complex dispute resolution workflow
- Background check API integration
- Dynamic pricing based on demand
- Chat/messaging between customer and provider
- Push notifications (Firebase Cloud Messaging)

### **🔮 Future Enhancements (Post-MVP)**

1. **Payment Integration**: Stripe/Razorpay for real transactions
2. **Advanced Analytics**: Revenue dashboards, booking trends
3. **Machine Learning**: Provider recommendations based on history
4. **Background Checks**: Integration with third-party verification APIs
5. **Dynamic Pricing**: Surge pricing during peak demand
6. **Mobile Apps**: React Native for iOS/Android
7. **Real-time Chat**: WebSocket-based messaging
8. **Provider Availability Calendar**: Google Calendar sync

---

## 🔒 Security Considerations

### **Implemented in MVP**

- ✅ **Password Hashing**: bcrypt with cost factor 12
- ✅ **JWT Tokens**: 24-hour expiration, HS256 algorithm
- ✅ **HTTPS**: Enforced in production (HTTP in dev)
- ✅ **SQL Injection Prevention**: Parameterized queries via SQLAlchemy
- ✅ **CORS**: Whitelist allowed origins only
- ✅ **Rate Limiting**: On `/auth` endpoints (10 req/min per IP)
- ✅ **Role-Based Access Control**: Middleware checks user role

### **Production Recommendations**

- 🔐 Store JWT secret in environment variable (never commit)
- 🔐 Use HTTPS with TLS 1.3
- 🔐 Implement refresh token rotation
- 🔐 Add CSRF protection for form submissions
- 🔐 Enable database encryption at rest
- 🔐 Add input validation on all endpoints
- 🔐 Set up logging and monitoring (Sentry, DataDog)

---

## 🐛 Troubleshooting

### **Database Connection Failed**

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# View logs
docker logs servicehub-postgres

# Reset database
docker-compose down -v
docker-compose up --build
```

### **CORS Errors in Frontend**

```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **JWT Token Not Persisting**

```typescript
// frontend/src/api/client.ts
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### **PostGIS Extension Not Found**

```sql
-- Connect to PostgreSQL as superuser
CREATE EXTENSION IF NOT EXISTS postgis;

-- Verify installation
SELECT PostGIS_Version();
```

---

## 📞 Support & Contact

- **Project Lead**: [Your Name] - [email@example.com]
- **Documentation**: [GitHub Wiki](https://github.com/your-org/servicehub/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-org/servicehub/issues)
- **Slack**: #servicehub-dev

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- **FastAPI**: Incredible async framework
- **PostGIS**: Making geospatial queries simple
- **React Team**: For the best UI library
- **Docker**: Simplifying deployments

---

**Built with ❤️ by Team ServiceHub**

*Last Updated: December 10, 2025*