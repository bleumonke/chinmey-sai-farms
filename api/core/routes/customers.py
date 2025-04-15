from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from daos import Customer
from models import CustomerCreate, CustomerResponse, CustomerUpdate

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.post("", response_model=CustomerResponse, status_code=201)
async def create_customer(
    customer_data: CustomerCreate,
    session: AsyncSession = Depends(get_session)
):
    dao = Customer(session)
    existing = await dao.exists(
        email=customer_data.email,
        phone=customer_data.phone
    )
    if existing:
        raise HTTPException(status_code=400, detail="Customer with this email or phone already exists")
    customer = await dao.create(**customer_data.model_dump())
    return customer.to_dict()


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: str,
    session: AsyncSession = Depends(get_session)
):
    customer = await Customer(session).get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=400, detail="Customer not found")
    return customer.to_dict()


@router.get("", response_model=list[CustomerResponse])
async def get_customers(
    session: AsyncSession = Depends(get_session)
):
    customers = await Customer(session).list_all()
    return [customer.to_dict() for customer in customers]

@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    customer_data: CustomerUpdate,
    session: AsyncSession = Depends(get_session)
):
    customer = await Customer(session).update(customer_id, **customer_data.model_dump())
    if not customer:
        raise HTTPException(status_code=400, detail="Customer not found")
    return customer.to_dict()

@router.delete("/{customer_id}", response_model=CustomerResponse)
async def delete_customer(
    customer_id: str,
    session: AsyncSession = Depends(get_session)
):
    customer = await Customer(session).delete(customer_id)
    if not customer:
        raise HTTPException(status_code=400, detail="Customer not found")
    return customer.to_dict()