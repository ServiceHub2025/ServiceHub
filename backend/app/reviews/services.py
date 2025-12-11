"""
Business logic for reviews.
"""
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from app.models import Review, Booking, ServiceProvider, BookingStatus, User
from app.schemas import ReviewCreate

class ReviewService:
    @staticmethod
    def create_review(
        db: Session,
        reviewer_id: UUID,
        review_in: ReviewCreate
    ) -> Review:
        """
        Create a new review and update provider rating.
        """
        # 1. Validate Booking
        booking = db.query(Booking).filter(Booking.id == review_in.booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        # 2. Check Permissions (Reviewer must be customer or provider involved)
        # Assuming for MVP: Customer reviews Provider.
        if booking.customer_id != reviewer_id:
             # What if provider reviews customer?
             if booking.provider.user_id != reviewer_id:
                 raise HTTPException(status_code=403, detail="Not authorized to review this booking")
        
        # 3. Check Status
        if booking.status != BookingStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Can only review completed bookings")
        
        # 4. Check if already reviewed (Review model has UNIQUE(booking_id))
        # Logic to distinguish WHO is reviewing whom?
        # The schema `Review` has `reviewer_id` and `reviewee_id` but `booking_id` is unique.
        # This implies ONE review per booking?
        # If so, it's typically Customer -> Provider.
        # If we want bidirectional, `booking_id` shouldn't be unique alone, or we valid uniqueness on (booking_id, reviewer_id).
        # Models.py says: `booking_id = Column(..., unique=True)`
        # This means ONLY ONE REVIEW PER BOOKING.
        # So we assume it's Customer -> Provider for MVP.
        
        if booking.customer_id == reviewer_id:
            reviewee_id = booking.provider.user_id # Provider's User ID
        else:
            reviewee_id = booking.customer_id
            
        # 5. Create Review
        review = Review(
            booking_id=review_in.booking_id,
            reviewer_id=reviewer_id,
            reviewee_id=reviewee_id,
            rating=review_in.rating,
            comment=review_in.comment
        )
        
        db.add(review)
        
        try:
            db.commit()
            db.refresh(review)
        except Exception:
            db.rollback()
            raise HTTPException(status_code=400, detail="Review already exists for this booking")

        # 6. Update Provider Rating (if reviewee is provider)
        # We need to find the provider profile associated with reviewee_id (User ID)
        # But wait, a User can have multiple provider profiles (one per service)?
        # Which one do we update? The one used in the booking!
        if booking.provider_id:
            # Re-calculate average
            # We want average of all reviews received by this provider user...
            # BUT `ServiceProvider` table has `rating`.
            # Is the rating per User, or per ServiceProvider profile?
            # Schema: ServiceProvider has `rating`.
            # We should query reviews for this Booking's Provider Profile?
            # Review table links to User (reviewee_id).
            # So if I review the User, it affects ALL their profiles?
            # Or should we link Review to ServiceProvider?
            # Current schema `Review` links to `User`.
            # So `ServiceProvider.rating` must be an aggregation of reviews where `reviewee_id == ServiceProvider.user_id`.
            # Let's aggregate all reviews for this user.
            
            # Note: This aggregates across services if user has multiple. Acceptable for MVP.
            
            avg_rating = db.query(func.avg(Review.rating)).filter(
                Review.reviewee_id == reviewee_id
            ).scalar()
            
            if avg_rating:
                # Update specific provider profile used in booking
                # Or all profiles? Usually one "Provider Reputation".
                # Let's update the one used.
                provider_profile = db.query(ServiceProvider).filter(
                    ServiceProvider.id == booking.provider_id
                ).first()
                
                if provider_profile:
                    provider_profile.rating = round(float(avg_rating), 2)
                    db.commit()
        
        return review
