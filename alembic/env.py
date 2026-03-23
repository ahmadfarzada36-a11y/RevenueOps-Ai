import asyncio
import sys
import os
from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context

# مسیر پروژه
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings
from app.core.database import engine  # AsyncEngine حرفه‌ای
from app.db.base_class import Base
from app.models import lead, deal, followup_task, user, company

target_metadata = Base.metadata

# Logging
config = context.config
fileConfig(config.config_file_name)

def do_run_migrations(connection):
    """اجرای Migration"""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """نسخه آنلاین Async"""
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

def run_migrations_offline():
    """نسخه آفلاین"""
    url = settings.DATABASE_URL or (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
        f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
        f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

# اجرای اصلی
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())