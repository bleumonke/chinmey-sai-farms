from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from daos import LayoutDAO, PlotDAO
from models import LayoutCreate, LayoutUpdate, LayoutResponse, PlotResponse
from typing import List

router = APIRouter(
    prefix="/layouts",
    tags=["Layouts"]
)

@router.post("", response_model=LayoutResponse, status_code=201)
async def create_layout(
    layout_data: LayoutCreate,
    session: AsyncSession = Depends(get_session)
):
    layout = await LayoutDAO(session).create_layout(**layout_data.model_dump())
    if not layout:
        raise HTTPException(status_code=400, detail="Layout creation failed")
    return layout

@router.get("/{layout_id}", response_model=LayoutResponse)
async def get_layout(
    layout_id: str,
    session: AsyncSession = Depends(get_session)
):
    layout = await LayoutDAO(session).get_layout_by_id(layout_id)
    if not layout:
        raise HTTPException(status_code=400, detail="Layout not found")
    return layout

@router.get("", response_model=List[LayoutResponse])
async def get_all_layouts(
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    layouts = await LayoutDAO(session).get_all_layouts(limit=limit)
    return layouts

@router.patch("/{layout_id}", response_model=LayoutResponse)
async def update_layout(
    layout_id: str,
    layout_data: LayoutUpdate,
    session: AsyncSession = Depends(get_session)
):
    layout = await LayoutDAO(session).update_layout(layout_id, **layout_data.model_dump())
    if not layout:
        raise HTTPException(status_code=400, detail="Layout update failed")
    return layout

@router.get("/{layout_id}/plots", response_model=List[PlotResponse])
async def get_layout_plots(
    layout_id: str,
    session: AsyncSession = Depends(get_session)
):
    plots = await PlotDAO(session).get_plots_by_layout_id(layout_id)
    if not plots:
        raise HTTPException(status_code=400, detail="No plots found for this layout")
    return plots