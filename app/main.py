import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import logger
from app.core.error_handler import register_exception_handlers
from app.core.tenant_middleware import TenantMiddleware

from app.api.v1 import auth
from app.api.v1 import users
from app.api.v1 import deals
from app.api.v1 import followups
from app.api.v1 import ai_messages
from app.api.v1 import revenue_prediction
from app.api.v1 import customers
from app.api.v1.dashboard import router as dashboard_router


def create_application() -> FastAPI:
    """
    Application factory
    """

    app = FastAPI(
        title="RevenueOps AI",
        description="AI powered deal recovery & sales follow-up automation",
        version="1.0.0"
    )

    # ---------------------------
    # Middleware
    # ---------------------------

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(TenantMiddleware)

    # ---------------------------
    # Error Handlers
    # ---------------------------

    register_exception_handlers(app)

    # ---------------------------
    # Routers
    # ---------------------------

    routers = [
        auth.router,
        users.router,
        deals.router,
        followups.router,
        ai_messages.router,
        revenue_prediction.router,
        customers.router
    ]

    for router in routers:
        app.include_router(router)

    app.include_router(
        dashboard_router,
        prefix="/api/dashboard",
        tags=["Dashboard"]
    )

    # ---------------------------
    # Health Check
    # ---------------------------

    @app.get("/")
    async def root():
        return {
            "status": "RevenueOps AI running",
            "version": "1.0.0"
        }

    # ---------------------------
    # Startup Event
    # ---------------------------

    @app.on_event("startup")
    async def startup_event():
        logger.info("RevenueOps AI backend started")

    # ---------------------------
    # Shutdown Event
    # ---------------------------

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("RevenueOps AI backend shutting down")

    return app


# Application instance
app = create_application()


if __name__ == "__main__":

    logger.info("Starting RevenueOps AI with Uvicorn")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )