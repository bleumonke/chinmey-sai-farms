from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from daos import PaymentMode as PaymentModeDAO
from models import PaymentModeCreate, PaymentModeResponse

router = APIRouter(
    prefix="/payment_modes",
    tags=["Payment Mode"]
)

@router.get("", response_model=list[PaymentModeResponse])
async def get_payment_modes(session: AsyncSession = Depends(get_session)):
    payment_modes = await PaymentModeDAO(session).list_all()
    return [payment_mode.to_dict() for payment_mode in payment_modes]

@router.get("/{payment_mode_id}", response_model=PaymentModeResponse)
async def get_payment_mode(payment_mode_id: str, session: AsyncSession = Depends(get_session)):
    payment_mode = await PaymentModeDAO(session).get_by_id(payment_mode_id)
    if not payment_mode:
        raise HTTPException(status_code=400, detail="No payment mode found for this ID")
    return payment_mode.to_dict()

@router.post("", response_model=PaymentModeResponse)
async def create_payment_mode(payment_mode: PaymentModeCreate, session: AsyncSession = Depends(get_session)):
    payment_mode = await PaymentModeDAO(session).create(**payment_mode.model_dump())
    if not payment_mode:
        raise HTTPException(status_code=400, detail="Failed to create payment mode")
    return payment_mode.to_dict()

@router.patch("/{payment_mode_id}", response_model=PaymentModeResponse)
async def update_payment_mode(payment_mode_id: str, payment_mode: PaymentModeCreate, session: AsyncSession = Depends(get_session)):
    payment_mode = await PaymentModeDAO(session).update(payment_mode_id, **payment_mode.model_dump())
    if not payment_mode:
        raise HTTPException(status_code=400, detail="No payment mode found for this ID")
    return payment_mode.to_dict()

@router.delete("/{payment_mode_id}", status_code=204)
async def delete_payment_mode(payment_mode_id: str, session: AsyncSession = Depends(get_session)):
    payment_mode = await PaymentModeDAO(session).delete(payment_mode_id)
    if not payment_mode:
        raise HTTPException(status_code=400, detail="No payment mode found for this ID")