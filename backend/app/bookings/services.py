"""
Business logic for bookings.
"""
from typing import List, Optional
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException, status

from app.models import Booking, ServiceProvider, BookingStatus, Service
from app.schemas import BookingCreate

class BookingService:
    @staticmethod
    def calculate_price(hourly_rate: float, hours: int) -> float:
        """Calculate total price including 15% commission."""
        base_cost = hourly_rate * hours
        total = base_cost * 1.15
        return round(total, 2)

    @staticmethod
    def check_overlap(
        db: Session, 
        provider_id: UUID, 
        start_time: datetime, 
        hours: int
    ) -> bool:
        """
        Check if provider has overlapping bookings.
        Returns True if overlap exists.
        """
        end_time = start_time + timedelta(hours=hours)
        
        # Overlap condition: (StartA < EndB) and (EndA > StartB)
        # We check against any booking that is NOT Cancelled or Completed (maybe?).
        # Actually, Completed bookings take up time in the past, but for future bookings?
        # If I look at history, verified providers shouldn't have overlaps.
        # But we mostly care about future.
        # States that block availability: REQUESTED, ACCEPTED, IN_PROGRESS.
        # (Assuming strict blocking).
        
        overlapping_booking = db.query(Booking).filter(
            Booking.provider_id == provider_id,
            Booking.status.in_([
                BookingStatus.REQUESTED, 
                BookingStatus.ACCEPTED, 
                BookingStatus.IN_PROGRESS
            ]),
            Booking.scheduled_time < end_time,
            func_booking_end_time(Booking.scheduled_time, Booking.hours) > start_time
        ).first()
        
        return overlapping_booking is not None

    @staticmethod
    def create_booking(
        db: Session,
        customer_id: UUID,
        booking_in: BookingCreate
    ) -> Booking:
        """Create a new booking."""
        
        # 1. Get Provider to check rate and existence
        provider = db.query(ServiceProvider).filter(ServiceProvider.id == booking_in.provider_id).first()
        if not provider:
            raise HTTPException(status_code=404, detail="Provider not found")
            
        # 2. Validate Service match?
        # BookingCreate has service_id. Provider must verify they offer this service?
        # The schema implies Provider is linked to ONE service_id.
        if provider.service_id != booking_in.service_id:
             raise HTTPException(status_code=400, detail="Provider does not offer this service")

        # 3. Check Overlap
        # Note: SQLAlchemy hybrid properties or expression needed for end_time query
        # Since I can't easily use custom func in filter without definition, 
        # I'll implement a slightly different overlap query or fetch candidates.
        # Efficient way:
        # filter(provider_id == ...).all() then check in python? 
        # OR generic SQL filter: scheduled_time < end AND scheduled_time + interval '1 hour' * hours > start
        
        # Let's do a raw filter for "scheduled_time + hours * interval"
        # Since DB is Postgres, we can us SQL expressions.
        # But for MVP simplicity/safety with ORM:
        # We can implement check_overlap using logic below `create_booking` or inline.
        
        # Re-implementing check_overlap logic inline with ORM safe approach:
        # We need `Booking.scheduled_time + Booking.hours * timedelta(...)` ?
        # No, Booking.hours is int.
        # Let's use Python iteration for safety if volume is low (MVP), 
        # or properly construct the query.
        
        # Proper query approach:
        # We want to find bookings where:
        # existing_start < new_end AND existing_end > new_start
        
        new_start = booking_in.scheduled_time
        new_end = new_start + timedelta(hours=booking_in.hours)
        
        # Fetch potential conflicts (same day?) or just all active for provider
        # Optimization: filter by date range roughly
        potential_conflicts = db.query(Booking).filter(
            Booking.provider_id == booking_in.provider_id,
            Booking.status.in_([BookingStatus.REQUESTED, BookingStatus.ACCEPTED, BookingStatus.IN_PROGRESS]),
            Booking.scheduled_time >= new_start - timedelta(hours=8), # Look back max possible duration
            Booking.scheduled_time <= new_end
        ).all()
        
        for b in potential_conflicts:
            b_end = b.scheduled_time + timedelta(hours=b.hours)
            if b.scheduled_time < new_end and b_end > new_start:
                raise HTTPException(status_code=409, detail="Provider is already booked for this time slot")

        # 4. Calculate Price
        total_amount = BookingService.calculate_price(provider.hourly_rate, booking_in.hours)
        
        # 5. Create
        booking = Booking(
            customer_id=customer_id,
            provider_id=booking_in.provider_id,
            service_id=booking_in.service_id,
            status=BookingStatus.REQUESTED,
            scheduled_time=booking_in.scheduled_time,
            hours=booking_in.hours,
            total_amount=total_amount
        )
        
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def get_user_bookings(db: Session, user_id: UUID, role: str) -> List[Booking]:
        """Get bookings for a user based on role."""
        if role == "customer": # Compare with string or Enum value
            return db.query(Booking).filter(Booking.customer_id == user_id).order_by(Booking.scheduled_time.desc()).all()
        elif role == "provider":
            # For provider, we need to find the provider profile id first?
            # Or does 'user_id' map? 
            # Booking has 'provider_id' which is key to 'service_providers.id', NOT 'users.id'.
            # So we need to join or look up.
            return db.query(Booking).join(ServiceProvider).filter(ServiceProvider.user_id == user_id).order_by(Booking.scheduled_time.desc()).all()
        return []

    @staticmethod
    def update_booking_status(
        db: Session,
        booking_id: UUID,
        new_status: BookingStatus,
        user_id: UUID,
        user_role: str
    ) -> Booking:
        """
        Update booking status with state machine validation.
        """
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Permission Check (Basic) - Ensure user is involved in booking
        # We need to check if user.id matches customer_id or provider.user.id
        # Ideally, we should join valid_users, but for efficiency:
        
        is_customer = (booking.customer_id == user_id)
        # Check provider: needs join or separate query.
        # Let's trust user_role passed from route context if we trust the auth dependency to be correct.
        # But for strictly validating "Is this THE provider for this booking?", we check:
        # provider = db.query(ServiceProvider).filter(ServiceProvider.id == booking.provider_id).first()
        # is_provider = (provider.user_id == user_id)
        
        # More efficient:
        # If role is provider, check if booking.provider.user_id == user_id
        is_provider = False
        if user_role == "provider":
            provider = db.query(ServiceProvider).filter(ServiceProvider.id == booking.provider_id).first()
            if provider and provider.user_id == user_id:
                is_provider = True
        
        if not (is_customer or is_provider):
             # Admin could be allowed too, but MVP doesn't specify admin booking mgmt
             raise HTTPException(status_code=403, detail="Not authorized to modify this booking")

        current_status = booking.status
        
        # State Machine Logic
        # Transitions:
        # REQUESTED -> ACCEPTED (Provider only), CANCELLED (Customer/Provider)
        # ACCEPTED -> IN_PROGRESS (Provider), CANCELLED (Customer/Provider - maybe with penalty?)
        # IN_PROGRESS -> COMPLETED (Provider)
        
        valid = False
        
        if current_status == BookingStatus.REQUESTED:
            if new_status == BookingStatus.ACCEPTED and is_provider:
                valid = True
            elif new_status == BookingStatus.CANCELLED:
                valid = True # Both can cancel request
        
        elif current_status == BookingStatus.ACCEPTED:
            if new_status == BookingStatus.IN_PROGRESS and is_provider:
                valid = True
            elif new_status == BookingStatus.CANCELLED:
                valid = True # Both can cancel (MVP simplified)

        elif current_status == BookingStatus.IN_PROGRESS:
            if new_status == BookingStatus.COMPLETED and is_provider:
                valid = True
        
        if not valid:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid status transition from {current_status} to {new_status} by {user_role}"
            )
            
        booking.status = new_status
        db.commit()
        db.refresh(booking)
        return booking
