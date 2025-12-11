"""
ServiceHub FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine
from app.models import Base

# Create FastAPI app
app = FastAPI(
    title="ServiceHub API",
    description="On-demand home services marketplace API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print("🚀 ServiceHub API starting up...")
    print(f"📊 Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Not configured'}")
    print(f"🔒 CORS Origins: {settings.cors_origins}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print("👋 ServiceHub API shutting down...")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "ServiceHub API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "api": "operational"
    }


# Routers
from app.providers import routes as provider_routes
from app.bookings import routes as booking_routes
from app.reviews import routes as review_routes

app.include_router(provider_routes.router)
app.include_router(booking_routes.router)
app.include_router(review_routes.router)

# TODO: Import and include routers from auth, admin
# from app.auth import routes as auth_routes
# app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
