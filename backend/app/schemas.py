from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime
from enum import Enum

# --- Shared Enums ---
class UserRole(str, Enum):
    CUSTOMER = "customer"
    PROVIDER = "provider"
    ADMIN = "admin"

class BookingStatus(str, Enum):
    REQUESTED = "REQUESTED"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole

class UserCreate(UserBase):
    password: str
    phone: Optional[str] = None

class UserResponse(UserBase):
    id: UUID
    phone: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Service Schemas ---
class ServiceResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    base_price: float
    
    class Config:
        from_attributes = True

# --- Provider Schemas ---
class ProviderCreate(BaseModel):
    service_id: int
    hourly_rate: float
    lat: float
    lon: float

class ProviderResponse(BaseModel):
    id: UUID
    user_id: UUID
    service_id: int
    hourly_rate: float
    verified: bool
    rating: float
    user: Optional[UserResponse] = None
    service: Optional[ServiceResponse] = None
    distance: Optional[float] = None  # Field for search results

    class Config:
        from_attributes = True

# --- Booking Schemas ---
class BookingCreate(BaseModel):
    provider_id: UUID
    service_id: int
    scheduled_time: datetime
    hours: int

    @validator('hours')
    def validate_hours(cls, v):
        if not 1 <= v <= 8:
            raise ValueError('Hours must be between 1 and 8')
        return v

class BookingUpdateStatus(BaseModel):
    status: BookingStatus

class BookingResponse(BaseModel):
    id: UUID
    customer_id: UUID
    provider_id: UUID
    service_id: int
    status: BookingStatus
    scheduled_time: datetime
    hours: int
    total_amount: float
    created_at: datetime
    
    # Nested responses could be added if needed
    
    class Config:
        from_attributes = True

# --- Review Schemas ---
class ReviewCreate(BaseModel):
    booking_id: UUID
    rating: int
    comment: Optional[str] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class ReviewResponse(BaseModel):
    id: UUID
    booking_id: UUID
    reviewer_id: UUID
    reviewee_id: UUID
    rating: int
    comment: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
