import traceback
import uuid

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

import app
from app.core.logger import get_logger


logger = get_logger("errors")


class ErrorHandlerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())

        try:
            response = await call_next(request)
            return response

        except Exception as exc:

            error_trace = traceback.format_exc()

            logger.error(
                f"""
REQUEST_ID: {request_id}
REQUEST: {request.method} {request.url}
CLIENT: {request.client.host if request.client else "unknown"}

ERROR: {str(exc)}

TRACEBACK:
{error_trace}
"""
            )

            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "request_id": request_id,
                    "detail": "An unexpected error occurred"
                }
            )
def register_exception_handlers(app: FastAPI):
    """
    Register global error middleware
    """
    app.add_middleware(ErrorHandlerMiddleware)