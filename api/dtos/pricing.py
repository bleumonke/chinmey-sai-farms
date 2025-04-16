from .base import Base
from sqlalchemy import Column, TIMESTAMP, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Pricing(Base):
    __tablename__ = "pricing"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop_id = Column(UUID(as_uuid=True), ForeignKey("crops.id"), nullable=False)
    payment_mode_id = Column(UUID(as_uuid=True), ForeignKey("payment_modes.id"), nullable=False)
    extent_range_id = Column(UUID(as_uuid=True), ForeignKey("extent_ranges.id"), nullable=False)
    cost_per_acre = Column(Float, nullable=True)
    cost_per_cent = Column(Float, nullable=True)
    cost_per_sqft = Column(Float, nullable=True)
    total_cost_per_acre = Column(Float, nullable=True)
    emi_per_month = Column(Float, nullable=True)
    valid_from = Column(TIMESTAMP(timezone=True), nullable=False)
    valid_to = Column(TIMESTAMP(timezone=True), nullable=False)