from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models import User, UserRole
from app.auth.dependencies import get_current_user, require_role
from app.schemas import ProviderCreate, ProviderResponse
from app.providers.services import ProviderService

router = APIRouter(prefix="/providers", tags=["providers"])

@router.post("/", response_model=ProviderResponse, status_code=status.HTTP_201_CREATED)
def register_provider(
    provider_in: ProviderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Register the current user as a service provider.
    """
    # Verify user is not already a provider? 
    # For simplicity, we'll let the service handle constraints (one profile per user-service pair?)
    # DB model has user_id as FK, but not strictly unique=True in the User table definition?
    # Wait, `provider_profiles = relationship...`. User can potentially have multiple profiles 
    # (e.g. Cleaner AND Plumber)?
    # Looking at models.py: ServiceProvider has `user_id` as FK. No unique constraint on user_id alone, 
    # but logically a user might offer multiple services. 
    # HOWEVER, the MVP spec says "Provider Profile" singular usually. 
    # Let's assume one profile per user for now, or just allow creation.
    
    # Check if this specific service profile already exists for user?
    existing = db.query(ProviderService.get_provider_by_user_id(db, current_user.id))
    # Wait, get_provider_by_user_id returns FIRST match.
    
    # Actually, `services.py` has `create_provider_profile`. Let's use that.
    provider = ProviderService.create_provider_profile(
        db=db,
        user_id=current_user.id,
        service_id=provider_in.service_id,
        hourly_rate=provider_in.hourly_rate,
        lat=provider_in.lat,
        lon=provider_in.lon
    )
    
    # We ideally want to update the user's role to PROVIDER if they were just a CUSTOMER?
    # Or maybe the UI handles that flow.
    # The handoff doc says "User model with role enum".
    
    return provider

@router.get("/search", response_model=List[ProviderResponse])
def search_providers(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    radius: float = Query(10.0, description="Radius in km (5, 10, 20)"),
    service_id: Optional[int] = Query(None, description="Filter by service ID"),
    db: Session = Depends(get_db)
):
    """
    Search for providers within a specific radius.
    """
    providers_with_dist = ProviderService.search_providers(
        db=db,
        lat=lat,
        lon=lon,
        radius_km=radius,
        service_id=service_id
    )
    
    # Transform to ProviderResponse
    results = []
    for provider, dist in providers_with_dist:
        # We need to attach the distance to the response model.
        # ProviderResponse has `distance: Optional[float]` field.
        # SQLAlchemy object `provider` won't have `distance` attribute by default unless we setattr,
        # but Pydantic's from_attributes (orm_mode) reads attributes.
        # Check if we can just construct the dict or if we need to modify the object.
        
        # Taking a safer approach: clone the object or use Pydantic construct
        p_data = ProviderResponse.from_orm(provider)
        p_data.distance = dist  # distance in meters from PostGIS
        results.append(p_data)
        
    return results
