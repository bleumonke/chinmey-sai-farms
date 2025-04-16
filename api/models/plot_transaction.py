from pydantic import BaseModel
from typing import Optional
import uuid

class PlotTransactionCreate(BaseModel):
    plot_id: uuid.UUID
    customer_id: uuid.UUID
    pricing_id: uuid.UUID
    purchase_date: str
    amount_invested: float
    sale_date: Optional[str] = None
    sale_amount: Optional[float] = None
    roi_percentage: Optional[float] = None


class PlotTransactionUpdate(BaseModel):
    plot_id: Optional[uuid.UUID] = None
    customer_id: Optional[uuid.UUID] = None
    pricing_id: Optional[uuid.UUID] = None
    purchase_date: Optional[str] = None
    amount_invested: Optional[float] = None
    sale_date: Optional[str] = None
    sale_amount: Optional[float] = None
    roi_percentage: Optional[float] = None

class PlotTransactionResponse(PlotTransactionUpdate):
    id: uuid.UUID
    model_config = {
        "from_attributes": True
    }