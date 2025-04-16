from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from daos import Crop as CropDAO
from models import CropCreate, CropResponse
import logging

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/crops",
    tags=["Crops"],
)

@router.get("/", response_model=list[CropResponse])
async def get_crops(
    session: AsyncSession = Depends(get_session)
):
    crops = await CropDAO(session).list_all()
    return [crop.to_dict() for crop in crops]

@router.get("/{crop_id}", response_model=CropResponse)
async def get_crop(
    crop_id: str,
    session: AsyncSession = Depends(get_session)
):
    crop = await CropDAO(session).get_by_id(crop_id)
    if not crop:
        raise HTTPException(status_code=400, detail="Crop not found")
    return crop.to_dict()

@router.post("/", response_model=CropResponse, status_code=201)
async def create_crop(
    crop_data: CropCreate,
    session: AsyncSession = Depends(get_session)
):
    dao = CropDAO(session)
    existing = await dao.exists(name=crop_data.name)
    if existing:
        raise HTTPException(status_code=400, detail="Crop with this name already exists")
    crop = await dao.create(**crop_data.model_dump())
    return crop.to_dict()

@router.patch("/{crop_id}", response_model=CropResponse)
async def update_crop(
    crop_id: str,
    crop_data: CropCreate,
    session: AsyncSession = Depends(get_session)
):
    updated_crop = await CropDAO(session).update(crop_id, **crop_data.model_dump())
    if not updated_crop:
        raise HTTPException(status_code=400, detail="Crop not found")
    return updated_crop.to_dict()

@router.delete("/{crop_id}", status_code=204)
async def delete_crop(
    crop_id: str,
    session: AsyncSession = Depends(get_session)
):
    deleted_crop = await CropDAO(session).delete(crop_id)
    if not deleted_crop:
        raise HTTPException(status_code=400, detail="Crop not found")