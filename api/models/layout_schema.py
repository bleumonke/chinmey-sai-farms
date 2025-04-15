from pydantic import BaseModel
from typing import Optional
import uuid

from .plot_schema import PlotResponse

class LayoutCreate(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    country: str
    area_in_acres: float
    center_coordinates: dict
    perimeter_coordinates: dict


class LayoutUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    area_in_acres: Optional[float] = None
    center_coordinates: Optional[dict] = None
    perimeter_coordinates: Optional[dict] = None


class LayoutResponse(LayoutUpdate):
    id: uuid.UUID

    class Config:
        from_attributes = True