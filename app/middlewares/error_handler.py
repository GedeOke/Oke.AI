"""
Global error handlers for the FastAPI application.
"""
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.ai.llm_provider import LLMProviderError
from app.db.supabase import SupabaseClientError
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _json_error(message: str, code: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"status": "error", "message": message, "code": code},
    )


def init_error_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers with the FastAPI app.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        return _json_error(
            message=str(exc.detail or "HTTP error"),
            code=f"ERR_HTTP_{exc.status_code}",
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logger.debug("Request validation error", extra={"errors": exc.errors()})
        return _json_error(
            message="Request validation failed.",
            code="ERR_REQUEST_VALIDATION",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(ValidationError)
    async def validation_handler(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        logger.debug("Validation error", extra={"errors": exc.errors()})
        return _json_error(
            message="Validation error.",
            code="ERR_VALIDATION",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(SupabaseClientError)
    async def supabase_error_handler(
        request: Request, exc: SupabaseClientError
    ) -> JSONResponse:
        logger.error("Supabase error", extra={"path": str(request.url)})
        return _json_error(
            message="Database service error.",
            code="ERR_SUPABASE",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    @app.exception_handler(LLMProviderError)
    async def llm_provider_error_handler(
        request: Request, exc: LLMProviderError
    ) -> JSONResponse:
        logger.error("LLM provider error", extra={"error": str(exc)})
        return _json_error(
            message=str(exc),
            code="ERR_LLM_PROVIDER",
            status_code=status.HTTP_502_BAD_GATEWAY,
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("Unhandled exception", extra={"path": str(request.url)})
        return _json_error(
            message="Internal server error.",
            code="ERR_INTERNAL_SERVER",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
