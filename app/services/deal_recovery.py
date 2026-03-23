from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.deal import Deal
from app.models.lead import Lead

from app.services.ai.revenue_prediction import predict_deal_probability
from app.services.followup_engine import generate_followup_action
from app.services.ai.message_generator import generate_followup_message

from app.services.email_service import send_email
from app.services.whatsapp_service import send_whatsapp
from app.services.linkedin_service import send_linkedin_message


class DealRecoveryEngine:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def recover(self, deal_id: str):

        # 🔥 گرفتن Deal
        result = await self.db.execute(
            select(Deal).where(Deal.id == deal_id)
        )
        deal = result.scalar_one_or_none()

        if not deal:
            return {"status": "deal_not_found"}

        # 🔥 گرفتن Lead
        lead_result = await self.db.execute(
            select(Lead).where(Lead.id == deal.lead_id)
        )
        lead = lead_result.scalar_one_or_none()

        if not lead:
            return {"status": "lead_not_found"}

        # 🔥 AI Prediction
        probability = predict_deal_probability({
            "amount": float(deal.deal_value),
            "interaction_count": 5,
            "days_open": 10
        })

        # 🔥 Action
        action = generate_followup_action(probability)

        message = f"""
Hi {lead.contact_person or ''},

We wanted to follow up regarding your interest.

{action}

Best regards,
Sales Team
"""

        # 🔥 ارسال واقعی
        if lead.email:
            await send_email(lead.email, "Follow-up", message)

        if lead.phone:
            await send_whatsapp(lead.phone, message)

        if hasattr(lead, "linkedin") and lead.linkedin:
            await send_linkedin_message(lead.linkedin, message)

        # 🔥 آپدیت Deal
        deal.notes = f"Follow-up sent | probability={probability}"
        await self.db.commit()

        return {
            "status": "success",
            "probability": probability
        }