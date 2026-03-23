from app.core.celery_app import celery
from app.services.deal_recovery import DealRecoveryEngine
from app.db.session import AsyncSessionLocal
from app.models.deal import Deal
from sqlalchemy import select


@celery.task(name="deal_recovery_task")
def deal_recovery_task(deal_id: str):

    import asyncio
    asyncio.run(_recover(deal_id))


async def _recover(deal_id: str):

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Deal).where(Deal.id == deal_id)
        )

        deal = result.scalar_one_or_none()

        if not deal:
            return

        engine = DealRecoveryEngine()

        await engine.recover(deal)