from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from typing import List
from daos import Pricing as PricingDAO
from models import PricingCreate, PricingUpdate, PricingResponse

router = APIRouter(
    prefix="/pricing",
    tags=["pricing"]
)

@router.get("", response_model=List[PricingResponse])
async def get_pricing(session: AsyncSession = Depends(get_session)):
    pricings = await PricingDAO(session).list_all()
    return [pricing.to_dict() for pricing in pricings]

@router.get("/{pricing_id}", response_model=PricingResponse)
async def get_pricing(pricing_id: str, session: AsyncSession = Depends(get_session)):
    pricing = await PricingDAO(session).get_by_id(pricing_id)
    if not pricing:
        raise HTTPException(status_code=400, detail="No pricing found with this ID")
    return pricing.to_dict()

@router.post("", response_model=PricingResponse)
async def create_pricing(pricing: PricingCreate, session: AsyncSession = Depends(get_session)):
    pricing_dao = await PricingDAO(session).create(**pricing.model_dump())
    if not pricing_dao:
        raise HTTPException(status_code=400, detail="Pricing could not be created")
    return pricing_dao.to_dict()

@router.patch("/{pricing_id}", response_model=PricingResponse)
async def update_pricing(pricing_id: str, pricing: PricingUpdate, session: AsyncSession = Depends(get_session)):
    pricing_dao = await PricingDAO(session).update(pricing_id, **pricing.model_dump())
    if not pricing_dao:
        raise HTTPException(status_code=400, detail="No pricing found with this ID")
    return pricing_dao.to_dict()

@router.delete("/{pricing_id}", status_code=204)
async def delete_pricing(pricing_id: str, session: AsyncSession = Depends(get_session)):
    pricing_dao = await PricingDAO(session).delete(pricing_id)
    if not pricing_dao:
        raise HTTPException(status_code=400, detail="No pricing found with this ID")