from pydantic import BaseModel
from typing import Optional
import uuid

class PlotCreate(BaseModel):
    number: str
    layout_id: uuid.UUID
    name: str
    area_in_acres: float
    perimeter_coordinates: dict
    is_sold: bool = False
    is_active: bool = True
    description: Optional[str] = None


class PlotUpdate(BaseModel):
    number: Optional[str] = None
    layout_id: Optional[str] = None
    name: Optional[str] = None
    area_in_acres: Optional[float] = None
    perimeter_coordinates: Optional[dict] = None
    is_sold: Optional[bool] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None

class PlotResponse(PlotUpdate):
    id: uuid.UUID
    model_config = {
        "from_attributes": True
    }