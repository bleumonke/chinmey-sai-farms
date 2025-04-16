from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from typing import List
from daos import PlotTransaction as PlotTransactionDAO
from models import PlotTransactionCreate, PlotTransactionUpdate, PlotTransactionResponse

router = APIRouter(
    prefix="/plot_transactions",
    tags=["plot_transactions"]
)

@router.get("", response_model=List[PlotTransactionResponse])
async def get_plot_transactions(session: AsyncSession = Depends(get_session)):
    plot_transactions = await PlotTransactionDAO(session).list_all()
    return [plot_transaction.to_dict() for plot_transaction in plot_transactions]

@router.get("/{plot_transaction_id}", response_model=PlotTransactionResponse)
async def get_plot_transaction(plot_transaction_id: str, session: AsyncSession = Depends(get_session)):
    plot_transaction = await PlotTransactionDAO(session).get_by_id(plot_transaction_id)
    if not plot_transaction:
        raise HTTPException(status_code=400, detail="No plot transaction found with this ID")
    return plot_transaction.to_dict()

@router.post("", response_model=PlotTransactionResponse)
async def create_plot_transaction(plot_transaction: PlotTransactionCreate, session: AsyncSession = Depends(get_session)):
    plot_transaction_dao = await PlotTransactionDAO(session).create(**plot_transaction.model_dump())
    if not plot_transaction_dao:
        raise HTTPException(status_code=400, detail="Plot transaction could not be created")
    return plot_transaction_dao.to_dict()

@router.patch("/{plot_transaction_id}", response_model=PlotTransactionResponse)
async def update_plot_transaction(plot_transaction_id: str, plot_transaction: PlotTransactionUpdate, session: AsyncSession = Depends(get_session)):
    plot_transaction_dao = await PlotTransactionDAO(session).update(plot_transaction_id, **plot_transaction.model_dump())
    if not plot_transaction_dao:
        raise HTTPException(status_code=400, detail="No plot transaction found with this ID")
    return plot_transaction_dao.to_dict()

@router.delete("/{plot_transaction_id}", status_code=204)
async def delete_plot_transaction(plot_transaction_id: str, session: AsyncSession = Depends(get_session)):
    plot_transaction_dao = await PlotTransactionDAO(session).delete(plot_transaction_id)
    if not plot_transaction_dao:
        raise HTTPException(status_code=400, detail="No plot transaction found with this ID")