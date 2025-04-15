from .base_dto import BaseDTO
from sqlalchemy import func, Column, String, TIMESTAMP, JSON, Boolean, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

class PlotDTO(BaseDTO):
    __tablename__ = "plots"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    layout_id = Column(UUID(as_uuid=True), ForeignKey("layouts.id", ondelete="CASCADE"), nullable=False)
    number = Column(String(20), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    area_in_acres = Column(Float, nullable=False)
    perimeter_coordinates = Column(JSON, nullable=False)
    is_sold = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)