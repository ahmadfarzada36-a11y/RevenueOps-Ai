from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # =========================
    # App
    # =========================
    APP_NAME: str
    ENVIRONMENT: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # =========================
    # Database
    # =========================
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str | None = None

    # =========================
    # Redis
    # =========================
    REDIS_URL: str

    # =========================
    # Email
    # =========================
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    # =========================
    # WhatsApp
    # =========================
    WHATSAPP_API_URL: str
    WHATSAPP_TOKEN: str

    # =========================
    # AI
    # =========================
    AI_PROVIDER: str
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "allow"  # اجازه می‌دهد فیلدهای اضافی خطا ندهند

    # روش حرفه‌ای برای ساخت DATABASE_URL از فیلدهای جدا
    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()