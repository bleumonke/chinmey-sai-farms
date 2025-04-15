from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from daos import Plot
from models import PlotCreate, PlotUpdate, PlotResponse

router = APIRouter(
    prefix="/plots",
    tags=["Plots"]
)

@router.post("/", response_model=PlotResponse)
async def create_plot(plot_data: PlotCreate, session: AsyncSession = Depends(get_session)):
    created_plot = await Plot(session).create(**plot_data.model_dump())
    if not created_plot:
        raise HTTPException(status_code=400, detail="Plot creation failed")
    return created_plot

@router.get("/{plot_id}", response_model=PlotResponse)
async def get_plot(plot_id: int, session: AsyncSession = Depends(get_session)):
    plot = await Plot(session).get_by_id(plot_id)
    if not plot:
        raise HTTPException(status_code=404, detail="Plot not found")
    return plot

@router.patch("/{plot_id}", response_model=PlotResponse)
async def update_plot(plot_id: int, plot_data: PlotUpdate, session: AsyncSession = Depends(get_session)):
    updated_plot = await Plot(session).update(plot_id, **plot_data.model_dump())
    if not updated_plot:
        raise HTTPException(status_code=404, detail="Plot not found")
    return updated_plot

@router.delete("/{plot_id}", response_model=PlotResponse)
async def delete_plot(plot_id: int, session: AsyncSession = Depends(get_session)):
    deleted_plot = await Plot(session).delete(plot_id)
    if not deleted_plot:
        raise HTTPException(status_code=404, detail="Plot not found")
    return deleted_plot