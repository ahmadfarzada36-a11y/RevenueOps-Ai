from app.core.celery_app import celery
from app.services.linkedin_service import LinkedInService
from app.services.ai.message_generator import generate_followup_message
from app.db.session import AsyncSessionLocal
from app.models.deal import Deal
from sqlalchemy import select


@celery.task(name="send_linkedin_followup_task")
def send_linkedin_followup_task(deal_id: str):

    import asyncio
    asyncio.run(_send_linkedin(deal_id))


async def _send_linkedin(deal_id: str):

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Deal).where(Deal.id == deal_id)
        )

        deal = result.scalar_one_or_none()

        if not deal:
            return

        message = await generate_followup_message(
            deal.lead.company_name,
            deal.lead.contact_person,
            deal.deal_value
        )

        linkedin = LinkedInService()

        await linkedin.send_message(
            profile_id=deal.lead.contact_person,
            message=message
        )