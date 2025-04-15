from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from daos import ExtentRange
from models import ExtentRangeCreate, ExtentRangeResponse, ExtentRangeUpdate

router = APIRouter(
    prefix="/extent_ranges",
    tags=["Extent Ranges"]
)

@router.post("/", response_model=ExtentRangeResponse, status_code=201)
async def create_extent_range(
    extent_range_data: ExtentRangeCreate,
    session: AsyncSession = Depends(get_session)
):
    dao = ExtentRange(session)
    extent_range = await dao.create(**extent_range_data.model_dump())
    return extent_range.to_dict()

@router.get("/{extent_range_id}", response_model=ExtentRangeResponse)
async def get_extent_range(
    extent_range_id: str,
    session: AsyncSession = Depends(get_session)
):
    extent_range = await ExtentRange(session).get_by_id(extent_range_id)
    if not extent_range:
        raise HTTPException(status_code=400, detail="Extent Range not found")
    return extent_range.to_dict()

@router.get("/", response_model=list[ExtentRangeResponse])
async def get_extent_ranges(
    session: AsyncSession = Depends(get_session)
):
    extent_ranges = await ExtentRange(session).list_all()
    return [extent_range.to_dict() for extent_range in extent_ranges]

@router.patch("/{extent_range_id}", response_model=ExtentRangeResponse)
async def update_extent_range(
    extent_range_id: str,
    extent_range_data: ExtentRangeUpdate,
    session: AsyncSession = Depends(get_session)
):
    extent_range = await ExtentRange(session).update(extent_range_id, **extent_range_data.model_dump())
    if not extent_range:
        raise HTTPException(status_code=400, detail="Extent Range not found")
    return extent_range.to_dict()

@router.delete("/{extent_range_id}", response_model=ExtentRangeResponse)
async def delete_extent_range(
    extent_range_id: str,
    session: AsyncSession = Depends(get_session)
):
    extent_range = await ExtentRange(session).delete(extent_range_id)
    if not extent_range:
        raise HTTPException(status_code=400, detail="Extent Range not found")
    return extent_range.to_dict()