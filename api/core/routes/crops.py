from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from daos import Crop
from models import CropCreate, CropResponse

router = APIRouter(
    prefix="/crops",
    tags=["Crops"]
)

@router.post("/", response_model=CropResponse, status_code=201)
async def create_crop(
    crop_data: CropCreate,
    session: AsyncSession = Depends(get_session)
):
    dao = Crop(session)
    crop = await dao.create(**crop_data.model_dump())
    return crop.to_dict()

@router.get("/{crop_id}", response_model=CropResponse)
async def get_crop(
    crop_id: str,
    session: AsyncSession = Depends(get_session)
):
    crop = await Crop(session).get_by_id(crop_id)
    if not crop:
        raise HTTPException(status_code=400, detail="Crop not found")
    return crop.to_dict()

@router.get("/", response_model=list[CropResponse])
async def get_crops(
    session: AsyncSession = Depends(get_session)
):
    crops = await Crop(session).list_all()
    return [crop.to_dict() for crop in crops]

@router.patch("/{crop_id}", response_model=CropResponse)
async def update_crop(
    crop_id: str,
    crop_data: CropCreate,
    session: AsyncSession = Depends(get_session)
):
    crop = await Crop(session).update(crop_id, **crop_data.model_dump())
    if not crop:
        raise HTTPException(status_code=400, detail="Crop not found")
    return crop.to_dict()

@router.delete("/{crop_id}", response_model=CropResponse)
async def delete_crop(
    crop_id: str,
    session: AsyncSession = Depends(get_session)
):
    crop = await Crop(session).delete(crop_id)
    if not crop:
        raise HTTPException(status_code=400, detail="Crop not found")
    return crop.to_dict()