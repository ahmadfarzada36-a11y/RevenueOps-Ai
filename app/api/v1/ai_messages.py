from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.ai_message import AIMessage
from app.schemas.ai_message import AIMessageCreate, AIMessageRead
from app.core.security import get_current_user
from app.models.user import User

from app.services.ai.ai_service import generate_followup_message


router = APIRouter(prefix="/ai-messages", tags=["AI Messages"])


@router.post("/generate", response_model=AIMessageRead)
async def generate_ai_message(
    lead_id: str,
    customer_name: str,
    deal_stage: str,
    channel: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    message = generate_followup_message(
        customer_name,
        deal_stage
    )

    ai_message = AIMessage(
        tenant_id=current_user.tenant_id,
        lead_id=lead_id,
        channel=channel,
        content=message
    )

    db.add(ai_message)

    await db.commit()
    await db.refresh(ai_message)

    return ai_message