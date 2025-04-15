from .base import Base
from sqlalchemy import func, Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid

class PaymentMode(Base):
    __tablename__ = "payment_modes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)