from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.deal import Deal, DealStatusEnum
from app.models.followup_task import FollowUpTask, FollowUpStatusEnum

# پارامترهای قابل تغییر
FOLLOWUP_DAYS_QUOTED = 3
HIGH_RISK_DAYS = 7
MEDIUM_RISK_DAYS = 5
DEAL_VALUE_THRESHOLD = 10000

async def check_deals_and_create_followups(db: AsyncSession):
    now = datetime.utcnow()
    
    # فقط Dealهای Quoted یا Follow-up
    result = await db.execute(select(Deal).where(Deal.status.in_([DealStatusEnum.Quoted, DealStatusEnum.FollowUp])))
    deals = result.scalars().all()

    for deal in deals:
        days_since_last_contact = (now - deal.last_contact_date).days if deal.last_contact_date else None

        # ایجاد Follow-up Task فقط اگر نیاز باشد
        if days_since_last_contact is None or days_since_last_contact >= FOLLOWUP_DAYS_QUOTED:
            task = FollowUpTask(
                tenant_id=deal.tenant_id,
                deal_id=deal.id,
                assigned_user_id=deal.assigned_user_id,
                due_date=now + timedelta(days=1),
                status=FollowUpStatusEnum.Pending
            )
            db.add(task)

        # تشخیص ریسک
        risk = "Low"
        if deal.deal_value > DEAL_VALUE_THRESHOLD and (days_since_last_contact is None or days_since_last_contact >= HIGH_RISK_DAYS):
            risk = "High"
        elif days_since_last_contact is None or days_since_last_contact >= MEDIUM_RISK_DAYS:
            risk = "Medium"

        # اضافه کردن risk به notes بدون پاک شدن متن قبلی
        deal.notes = (deal.notes or "") + f"\nRisk: {risk}"

    await db.commit()