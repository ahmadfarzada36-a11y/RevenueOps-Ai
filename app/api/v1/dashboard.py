# app/api/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.lead import Lead
from app.models.deal import Deal
from sqlalchemy.future import select
from datetime import datetime  # <-- اضافه شد

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

@router.get("/dashboard/overview")
async def dashboard_overview(db: AsyncSession = Depends(get_db)):
    total_leads = await db.execute(select(Lead))
    total_leads_count = len(total_leads.scalars().all())

    total_deals = await db.execute(select(Deal))
    deals = total_deals.scalars().all()
    deals_won = len([d for d in deals if d.status == "Won"])
    deals_lost = len([d for d in deals if d.status == "Lost"])
    followups_due = len([d for d in deals if d.next_follow_up_date <= datetime.utcnow() and d.status in ("Quoted","Follow-up")])

    return {
        "total_leads": total_leads_count,
        "deals_won": deals_won,
        "deals_lost": deals_lost,
        "followups_due_today": followups_due
    }