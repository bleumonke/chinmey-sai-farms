from pydantic import BaseModel
from typing import Optional
import uuid

class PricingCreate(BaseModel):
    crop_id: uuid.UUID
    payment_mode_id: uuid.UUID
    extent_range_id: uuid.UUID
    cost_per_acre: Optional[float] = None
    cost_per_cent: Optional[float] = None
    cost_per_sqft: Optional[float] = None
    total_cost_per_acre: Optional[float] = None
    emi_per_month: Optional[float] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None


class PricingUpdate(BaseModel):
    crop_id: Optional[uuid.UUID] = None
    payment_mode_id: Optional[uuid.UUID] = None
    extent_range_id: Optional[uuid.UUID] = None
    cost_per_acre: Optional[float] = None
    cost_per_cent: Optional[float] = None
    cost_per_sqft: Optional[float] = None
    total_cost_per_acre: Optional[float] = None
    emi_per_month: Optional[float] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None


class PricingResponse(PricingUpdate):
    id: uuid.UUID
    model_config = {
        "from_attributes": True
    }