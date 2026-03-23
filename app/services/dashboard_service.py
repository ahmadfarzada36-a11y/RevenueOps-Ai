from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.deal import Deal
from app.models.user import User

from app.services.ai.revenue_prediction import predict_deal_probability
from app.tasks.send_followups import send_followup_task

router = APIRouter()


@router.get("/")
async def dashboard_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 🔥 aggregation سریع
    result = await db.execute(
        select(
            func.count(Deal.id),
            func.sum(Deal.deal_value)
        ).where(Deal.tenant_id == current_user.tenant_id)
    )

    total_deals, total_value = result.one()

    # 🔥 deals محدود برای AI
    deals_result = await db.execute(
        select(Deal)
        .where(Deal.tenant_id == current_user.tenant_id)
        .limit(20)
    )

    deals = deals_result.scalars().all()

    high_risk = []
    high_potential = []

    for deal in deals:

        prob = predict_deal_probability({
            "amount": float(deal.deal_value),
            "interaction_count": 5,
            "days_open": 10
        })

        # 🔥 اگر ریسک بالا → trigger Celery
        if prob < 0.4:
            send_followup_task.delay(str(deal.id))

            high_risk.append({
                "deal_id": str(deal.id),
                "probability": prob,
                "action": "auto follow-up triggered"
            })

        elif prob > 0.7:
            high_potential.append({
                "deal_id": str(deal.id),
                "probability": prob
            })

    return {
        "total_deals": total_deals or 0,
        "total_value": float(total_value or 0),
        "high_risk_deals": high_risk,
        "high_potential_deals": high_potential
    }