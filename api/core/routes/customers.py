from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from daos import Customer as CustomerDAO
from models import CustomerCreate, CustomerUpdate, CustomerResponse
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("", response_model=CustomerResponse, status_code=201)
async def create_customer(
    customer_data: CustomerCreate,
    session: AsyncSession = Depends(get_session)
):
    dao = CustomerDAO(session)
    existing = await dao.exists(
        email=customer_data.email,
        phone=customer_data.phone
    )
    if existing:
        raise HTTPException(status_code=400, detail="Customer with this email or phone already exists")
    customer = await dao.create(**customer_data.model_dump())
    return customer.to_dict()

@router.get("", response_model=List[CustomerResponse])
async def get_customers(
    session: AsyncSession = Depends(get_session)
):
    customers = await CustomerDAO(session).list_all()
    return [customer.to_dict() for customer in customers]

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: str,
    session: AsyncSession = Depends(get_session)
):
    customer = await CustomerDAO(session).get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=400, detail="Customer not found")
    return customer.to_dict()

@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    customer_data: CustomerUpdate,
    session: AsyncSession = Depends(get_session)
):
    updated_customer = await CustomerDAO(session).update(customer_id, **customer_data.model_dump())
    if not updated_customer:
        raise HTTPException(status_code=400, detail="Customer not found")
    return updated_customer.to_dict()

@router.delete("/{customer_id}", status_code=204)
async def delete_customer(
    customer_id: str,
    session: AsyncSession = Depends(get_session)
):
    delete_customer = await CustomerDAO(session).delete(customer_id)
    if not delete_customer:
        raise HTTPException(status_code=400, detail="Customer not found")