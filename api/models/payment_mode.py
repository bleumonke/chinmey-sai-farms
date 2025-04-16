from pydantic import BaseModel
import uuid

class PaymentModeCreate(BaseModel):
    name: str

class PaymentModeResponse(PaymentModeCreate):
    id: uuid.UUID
    model_config = {
        "from_attributes": True
    }