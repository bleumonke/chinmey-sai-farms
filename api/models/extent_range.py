from pydantic import BaseModel
from typing import Optional
import uuid


class ExtentRangeCreate(BaseModel):
    label: str
    unit: str
    min_value: float
    max_value: float
    description: Optional[str] = None

class ExtentRangeResponse(ExtentRangeCreate):
    id: uuid.UUID

    class Config:
        orm_mode = True

class ExtentRangeUpdate(BaseModel):
    label: Optional[str] = None
    unit: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    description: Optional[str] = None