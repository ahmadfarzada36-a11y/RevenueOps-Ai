from celery import Celery
from app.core.config import settings


celery_app = Celery(
    "revenueops_ai",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)


celery_app.conf.update(

    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    timezone="UTC",
    enable_utc=True,

    task_track_started=True,

    worker_prefetch_multiplier=1,

    task_acks_late=True,

    broker_connection_retry_on_startup=True,
)


celery_app.conf.task_routes = {
    "app.tasks.email_tasks.*": {"queue": "emails"},
    "app.tasks.linkedin_tasks.*": {"queue": "linkedin"},
    "app.tasks.recovery_tasks.*": {"queue": "recovery"
    },
    "app.tasks.revenue_intelligence.*": {"queue": "revenue_intelligence"},
}