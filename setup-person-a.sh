#!/bin/bash

echo "=================================================="
echo "🚀 ServiceHub - Person A Setup Script"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.yml not found!${NC}"
    echo "Please run this script from the servicehub root directory"
    exit 1
fi

echo -e "${BLUE}📋 Step 1: Initializing Git repository...${NC}"
git init
git add .
git commit -m "chore: initial project setup with backend and frontend structure

- Add FastAPI backend with SQLAlchemy models
- Add React + TypeScript frontend with Vite
- Configure Docker Compose for PostgreSQL, Redis, Backend, Frontend
- Add Alembic for database migrations
- Configure TailwindCSS for styling
- Add comprehensive README with team roadmap"

echo -e "${GREEN}✅ Git repository initialized${NC}"
echo ""

echo -e "${BLUE}📋 Step 2: Setting up environment files...${NC}"
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Generate SECRET_KEY
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
if [ -n "$SECRET_KEY" ]; then
    # Replace SECRET_KEY in backend .env
    sed -i.bak "s/your-super-secret-key-change-this-in-production-use-openssl-rand-hex-32/$SECRET_KEY/" backend/.env
    rm backend/.env.bak 2>/dev/null
    echo -e "${GREEN}✅ Generated secure SECRET_KEY${NC}"
else
    echo -e "${RED}⚠️  Could not generate SECRET_KEY automatically. Please update backend/.env manually${NC}"
fi

echo ""

echo -e "${BLUE}📋 Step 3: Creating backend virtual environment...${NC}"
cd backend
python3 -m venv venv
echo -e "${GREEN}✅ Virtual environment created at backend/venv${NC}"
cd ..
echo ""

echo -e "${BLUE}📋 Step 4: Creating feature branch...${NC}"
git checkout -b person-a-auth
echo -e "${GREEN}✅ Created branch: person-a-auth${NC}"
echo ""

echo "=================================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=================================================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Add GitHub remote:"
echo "   ${BLUE}git remote add origin https://github.com/YOUR_ORG/servicehub.git${NC}"
echo "   ${BLUE}git push -u origin main${NC}"
echo "   ${BLUE}git push -u origin person-a-auth${NC}"
echo ""
echo "2. Start Docker services:"
echo "   ${BLUE}docker-compose up --build${NC}"
echo ""
echo "3. Verify services:"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "4. Read SETUP_GUIDE.md for detailed instructions"
echo ""
echo "=================================================="
