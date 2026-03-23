import asyncio
from celery import shared_task
from sqlalchemy.future import select

from app.core.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.models.deal import Deal, DealStatusEnum
from app.services.email_service import send_email
from app.services.whatsapp_service import send_whatsapp_message
from app.services.linkedin_service import send_linkedin_message  # حرفه‌ای اضافه شد
from app.services.ai.message_generator import generate_followup_message  # AI پیام

# --- Celery Queue اختصاصی ---
celery_app.conf.task_routes.update({
    "app.tasks.revenue_intelligence.run_engine": {"queue": "revenue_intelligence"}
})

# --- گرفتن Deals در خطر ---
async def get_at_risk_deals(session):
    result = await session.execute(
        select(Deal).where(
            Deal.status.in_([DealStatusEnum.New, DealStatusEnum.FollowUp])
        )
    )
    return result.scalars().all()

# --- ارسال پیام به Lead ها ---
async def engage_client(client_info, deal):
    # تولید پیام AI
    message = generate_followup_message(deal, client_info)
    
    if client_info.email:
        await send_email(client_info.email, message)
    if client_info.phone:
        await send_whatsapp_message(client_info.phone, message)
    if getattr(client_info, "linkedin_profile", None):
        await send_linkedin_message(client_info.linkedin_profile, message)

# --- تسک اصلی Celery ---
@shared_task(name="app.tasks.revenue_intelligence.run_engine")
def run_revenue_intelligence():
    async def main():
        async with AsyncSessionLocal() as session:
            deals = await get_at_risk_deals(session)
            for deal in deals:
                lead_info = deal.lead
                await engage_client(lead_info, deal)

    asyncio.run(main())

# --- زمان‌بندی در Celery Beat ---
celery_app.conf.beat_schedule = {
    "revenue_intelligence_every_hour": {
        "task": "app.tasks.revenue_intelligence.run_engine",
        "schedule": 3600.0,  # هر ۱ ساعت یکبار اجرا
    }
}