from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from typing import List
from daos import Plot as PlotDAO
from models import PlotCreate, PlotUpdate, PlotResponse


router = APIRouter(
    prefix="/plots",
    tags=["plots"]
)

@router.get("", response_model=List[PlotResponse])
async def get_plots(session: AsyncSession = Depends(get_session)):
    plots = await PlotDAO(session).list_all()
    return [plot.to_dict() for plot in plots]

@router.get("/{plot_id}", response_model=PlotResponse)
async def get_plot(plot_id: str, session: AsyncSession = Depends(get_session)):
    plot = await PlotDAO(session).get_by_id(plot_id)
    if not plot:
        raise HTTPException(status_code=400, detail="No plot found with this ID")
    return plot.to_dict()

@router.post("", response_model=PlotResponse)
async def create_plot(plot: PlotCreate, session: AsyncSession = Depends(get_session)):
    plot_dao = await PlotDAO(session).create(**plot.model_dump())
    if not plot_dao:
        raise HTTPException(status_code=400, detail="Plot could not be created")
    return plot_dao.to_dict()

@router.patch("/{plot_id}", response_model=PlotResponse)
async def update_plot(plot_id: str, plot: PlotUpdate, session: AsyncSession = Depends(get_session)):
    plot_dao = await PlotDAO(session).update(plot_id, **plot.model_dump())
    if not plot_dao:
        raise HTTPException(status_code=400, detail="No plot found with this ID")
    return plot_dao.to_dict()

@router.delete("/{plot_id}", status_code=204)
async def delete_plot(plot_id: str, session: AsyncSession = Depends(get_session)):
    plot_dao = await PlotDAO(session).delete(plot_id)
    if not plot_dao:
        raise HTTPException(status_code=400, detail="No plot found with this ID")