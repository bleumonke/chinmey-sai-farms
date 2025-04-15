from .base import Base
from sqlalchemy import func, Column, String, TIMESTAMP, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

class ExtentRange(Base):
    __tablename__ = "extent_ranges"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    label = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    unit = Column(String(50), nullable=False)
    min_value = Column(Float, nullable=False)
    max_value = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)