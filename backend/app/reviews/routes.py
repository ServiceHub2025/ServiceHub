from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth.dependencies import get_current_user
from app.schemas import ReviewCreate, ReviewResponse
from app.reviews.services import ReviewService

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review_in: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a review for a completed booking.
    """
    return ReviewService.create_review(
        db=db,
        reviewer_id=current_user.id,
        review_in=review_in
    )
