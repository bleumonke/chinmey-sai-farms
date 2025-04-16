from pydantic import BaseModel
import uuid


class CropCreate(BaseModel):
    name: str

class CropResponse(CropCreate):
    id: uuid.UUID
    model_config = {
        "from_attributes": True
    }