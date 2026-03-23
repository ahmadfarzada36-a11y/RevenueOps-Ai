from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadRead
from app.core.security import hash_password, get_current_user
from app.models.user import User

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("/", response_model=LeadRead)
async def create_lead(
    lead: LeadCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_lead = Lead(
        **lead.dict(),
        tenant_id=current_user.tenant_id
    )

    db.add(new_lead)
    await db.commit()
    await db.refresh(new_lead)

    return new_lead


@router.get("/", response_model=list[LeadRead])
async def list_leads(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = await db.execute(
        select(Lead).where(Lead.tenant_id == current_user.tenant_id)
    )

    leads = result.scalars().all()
    return leads