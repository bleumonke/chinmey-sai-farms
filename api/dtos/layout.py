from .base import Base
from sqlalchemy import func, Column, String, TIMESTAMP, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Layout(Base):
    __tablename__ = "layouts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    address = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(20), nullable=False)
    country = Column(String(50), nullable=False)
    area_in_acres = Column(Float, nullable=False)
    center_coordinates = Column(JSON, nullable=False)
    perimeter_cordinates = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)