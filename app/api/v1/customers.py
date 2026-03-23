from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.customer import Customer
from app.models.user import User
from app.schemas.customer import CustomerCreate, CustomerRead

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", response_model=CustomerRead)
async def create_customer(
    data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    customer = Customer(
        tenant_id=current_user.tenant_id,
        **data.dict()
    )

    db.add(customer)
    await db.commit()
    await db.refresh(customer)

    return customer


@router.get("/", response_model=list[CustomerRead])
async def list_customers(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Customer).where(Customer.tenant_id == current_user.tenant_id)
    )

    return result.scalars().all()