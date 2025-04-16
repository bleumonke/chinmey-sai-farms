from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from daos import ExtentRange as ExtentRangeDAO
from models import ExtentRangeCreate, ExtentRangeResponse, ExtentRangeUpdate

router = APIRouter(
    prefix="/extent_ranges",
    tags=["Extent Ranges"],
)

@router.get("", response_model=list[ExtentRangeResponse])
async def get_extent_ranges(
    session: AsyncSession = Depends(get_session),
) -> list[ExtentRangeResponse]:
    extent_ranges = await ExtentRangeDAO(session).list_all()
    return [extent_range.to_dict() for extent_range in extent_ranges]

@router.get("/{extent_range_id}", response_model=ExtentRangeResponse)
async def get_extent_range(
    extent_range_id: str,
    session: AsyncSession = Depends(get_session),
) -> ExtentRangeResponse:
    extent_range = await ExtentRangeDAO(session).get_by_id(extent_range_id)
    if not extent_range:
        raise HTTPException(status_code=400, detail="Extent Range not found for this ID")
    return extent_range.to_dict()

@router.post("", response_model=ExtentRangeResponse, status_code=201)
async def create_extent_range(
    extent_range_data: ExtentRangeCreate,
    session: AsyncSession = Depends(get_session),
) -> ExtentRangeResponse:
    extent_range = await ExtentRangeDAO(session).create(**extent_range_data.model_dump())
    return extent_range.to_dict()

@router.patch("/{extent_range_id}", response_model=ExtentRangeResponse)
async def update_extent_range(
    extent_range_id: str,
    extent_range_data: ExtentRangeUpdate,
    session: AsyncSession = Depends(get_session),
) -> ExtentRangeResponse:
    updated_extent_range = await ExtentRangeDAO(session).update(extent_range_id, **extent_range_data.model_dump())
    if not updated_extent_range:
        raise HTTPException(status_code=400, detail="Extent Range not found for this ID")
    return updated_extent_range.to_dict()

@router.delete("/{extent_range_id}", status_code=204)
async def delete_extent_range(
    extent_range_id: str,
    session: AsyncSession = Depends(get_session),
) -> None:
    deleted_extent_range = await ExtentRangeDAO(session).delete(extent_range_id)
    if not deleted_extent_range:
        raise HTTPException(status_code=400, detail="Extent Range not found for this ID")