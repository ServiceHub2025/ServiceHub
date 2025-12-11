"""
SQLAlchemy ORM models for ServiceHub.
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, 
    Text, ForeignKey, CheckConstraint, Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
import enum

from app.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    CUSTOMER = "customer"
    PROVIDER = "provider"
    ADMIN = "admin"


class BookingStatus(str, enum.Enum):
    """Booking status enumeration."""
    REQUESTED = "REQUESTED"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class User(Base):
    """User model for customers, providers, and admins."""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    provider_profiles = relationship("ServiceProvider", back_populates="user")
    bookings_as_customer = relationship(
        "Booking", 
        foreign_keys="[Booking.customer_id]",
        back_populates="customer"
    )
    reviews_given = relationship(
        "Review",
        foreign_keys="[Review.reviewer_id]",
        back_populates="reviewer"
    )
    reviews_received = relationship(
        "Review",
        foreign_keys="[Review.reviewee_id]",
        back_populates="reviewee"
    )


class Service(Base):
    """Service catalog (Cleaning, Plumbing, etc.)."""
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    base_price = Column(Float, nullable=False)
    active = Column(Boolean, default=True)
    
    # Relationships
    providers = relationship("ServiceProvider", back_populates="service")
    bookings = relationship("Booking", back_populates="service")


class ServiceProvider(Base):
    """Provider profile with location and pricing."""
    __tablename__ = "service_providers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    hourly_rate = Column(Float, nullable=False)
    location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    verified = Column(Boolean, default=False)
    rating = Column(Float, default=0.0)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 5', name='check_rating_range'),
        CheckConstraint('hourly_rate > 0', name='check_positive_rate'),
    )
    
    # Relationships
    user = relationship("User", back_populates="provider_profiles")
    service = relationship("Service", back_populates="providers")
    bookings = relationship("Booking", back_populates="provider")


class Booking(Base):
    """Booking between customer and provider."""
    __tablename__ = "bookings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("service_providers.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    status = Column(SQLEnum(BookingStatus), nullable=False, default=BookingStatus.REQUESTED)
    scheduled_time = Column(DateTime, nullable=False)
    hours = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('hours >= 1 AND hours <= 8', name='check_hours_range'),
        CheckConstraint('total_amount > 0', name='check_positive_amount'),
    )
    
    # Relationships
    customer = relationship("User", foreign_keys=[customer_id], back_populates="bookings_as_customer")
    provider = relationship("ServiceProvider", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")
    review = relationship("Review", back_populates="booking", uselist=False)


class Review(Base):
    """Review submitted after booking completion."""
    __tablename__ = "reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"), unique=True, nullable=False)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    reviewee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )
    
    # Relationships
    booking = relationship("Booking", back_populates="review")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="reviews_given")
    reviewee = relationship("User", foreign_keys=[reviewee_id], back_populates="reviews_received")
