from pydantic import BaseModel
import uuid


class CropCreate(BaseModel):
    name: str

class CropResponse(CropCreate):
    id: uuid.UUID

    class Config:
        from_attributes = True