from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth.dependencies import get_current_user
from app.schemas import BookingCreate, BookingResponse, BookingUpdateStatus
from app.bookings.services import BookingService

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_in: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new booking.
    """
    return BookingService.create_booking(db, current_user.id, booking_in)

@router.get("/me", response_model=List[BookingResponse])
def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all bookings for the current user.
    """
    return BookingService.get_user_bookings(db, current_user.id, current_user.role)

@router.patch("/{booking_id}/status", response_model=BookingResponse)
def update_booking_status(
    booking_id: UUID,
    status_update: BookingUpdateStatus,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the status of a booking.
    """
    return BookingService.update_booking_status(
        db=db,
        booking_id=booking_id,
        new_status=status_update.status,
        user_id=current_user.id,
        user_role=current_user.role
    )
