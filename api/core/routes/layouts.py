from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from typing import List
from daos import (
    Layout as LayoutDAO, 
    Plot as PlotDAO
)
from models import LayoutCreate, LayoutUpdate, LayoutResponse, PlotResponse

router = APIRouter(
    prefix="/layouts",
    tags=["Layouts"]
)

@router.get("", response_model=List[LayoutResponse])
async def get_layouts(session: AsyncSession = Depends(get_session)):
    layouts = await LayoutDAO(session).list_all()
    return [layout.to_dict() for layout in layouts]

@router.get("/{layout_id}/plots", response_model=List[PlotResponse])
async def get_layout_plots(layout_id: str, session: AsyncSession = Depends(get_session)):
    plots = await PlotDAO(session).get_plots_by_layout_id(layout_id)
    return [plot.to_dict() for plot in plots]

@router.get("/{layout_id}", response_model=LayoutResponse)
async def get_layout(layout_id: str, session: AsyncSession = Depends(get_session)):
    layout = await LayoutDAO(session).get_by_id(layout_id)
    if not layout:
        raise HTTPException(status_code=400, detail="No layout found with this ID")
    return layout.to_dict()

@router.post("", response_model=LayoutResponse)
async def create_layout(layout: LayoutCreate, session: AsyncSession = Depends(get_session)):
    layout_dao = await LayoutDAO(session).create(**layout.model_dump())
    if not layout_dao:
        raise HTTPException(status_code=400, detail="Layout could not be created")
    return layout_dao.to_dict()

@router.patch("/{layout_id}", response_model=LayoutResponse)
async def update_layout(layout_id: str, layout: LayoutUpdate, session: AsyncSession = Depends(get_session)):
    layout_dao = await LayoutDAO(session).update(layout_id, **layout.model_dump())
    if not layout_dao:
        raise HTTPException(status_code=400, detail="No layout found with this ID")
    return layout_dao.to_dict()

@router.delete("/{layout_id}", status_code=204)
async def delete_layout(layout_id: str, session: AsyncSession = Depends(get_session)):
    layout_dao = await LayoutDAO(session).delete(layout_id)
    if not layout_dao:
        raise HTTPException(status_code=400, detail="No layout found with this ID")
