from .base import Base
from sqlalchemy import Column, TIMESTAMP, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

class PlotTransaction(Base):
    __tablename__ = "plot_transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plot_id = Column(UUID(as_uuid=True), ForeignKey("plots.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    pricing_id = Column(UUID(as_uuid=True), ForeignKey("pricing.id"), nullable=False)
    purchase_date = Column(TIMESTAMP(timezone=True), nullable=False)
    sale_date = Column(TIMESTAMP(timezone=True), nullable=True)
    sale_amount = Column(Float, nullable=True)
    amount_invested = Column(Float, nullable=False)
    roi_percentage = Column(Float, nullable=True)