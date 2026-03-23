from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import hash_password, get_current_user
from app.models.followup_task import FollowUpTask
from app.models.user import User
from app.schemas.followup_task import FollowUpTaskCreate, FollowUpTaskRead

router = APIRouter(prefix="/followups", tags=["followups"])


# Create follow-up task
@router.post("/", response_model=FollowUpTaskRead)
async def create_followup(
    task: FollowUpTaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_task = FollowUpTask(
        tenant_id=current_user.tenant_id,
        lead_id=task.lead_id,
        message=task.message,
        scheduled_at=task.scheduled_at,
        status=task.status
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return new_task


# List follow-ups for tenant
@router.get("/", response_model=list[FollowUpTaskRead])
async def list_followups(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = await db.execute(
        select(FollowUpTask).where(
            FollowUpTask.tenant_id == current_user.tenant_id
        )
    )

    return result.scalars().all()