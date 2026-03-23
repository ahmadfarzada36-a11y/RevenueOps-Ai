import asyncio

from app.core.celery_app import celery_app
from app.db.session import AsyncSessionLocal

from app.services.deal_recovery import DealRecoveryEngine


@celery_app.task
def send_followup_task(deal_id: str):

    async def run():
        async with AsyncSessionLocal() as db:
            engine = DealRecoveryEngine(db)
            await engine.recover(deal_id)

    asyncio.run(run())