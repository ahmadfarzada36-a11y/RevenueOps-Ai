from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import hash_password, get_current_user
from app.models.deal import Deal
from app.models.user import User
from app.schemas.deal import DealCreate, DealRead

router = APIRouter(prefix="/deals", tags=["deals"])


# Create deal
@router.post("/", response_model=DealRead)
async def create_deal(
    deal: DealCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_deal = Deal(
        tenant_id=current_user.tenant_id,
        lead_id=deal.lead_id,
        title=deal.title,
        value=deal.value,
        stage=deal.stage
    )

    db.add(new_deal)
    await db.commit()
    await db.refresh(new_deal)

    return new_deal


# List deals
@router.get("/", response_model=list[DealRead])
async def list_deals(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = await db.execute(
        select(Deal).where(
            Deal.tenant_id == current_user.tenant_id
        )
    )

    return result.scalars().all()