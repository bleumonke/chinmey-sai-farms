from pydantic import BaseModel
import uuid

class PaymentModeCreate(BaseModel):
    name: str

class PaymentModeResponse(PaymentModeCreate):
    id: uuid.UUID

    class Config:
        from_attributes = True