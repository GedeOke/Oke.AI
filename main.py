"""
FastAPI entrypoint for OkeAI.
"""
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.middlewares.error_handler import init_error_handlers
from app.routers import register_routers
from app.utils.logger import get_logger, setup_logging
from app.utils.rate_limiter import RateLimiter

settings = get_settings()
setup_logging(settings.log_level)
logger = get_logger(__name__)

rate_limiter = RateLimiter()


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.
    """
    application = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_error_handlers(application)
    register_middlewares(application)
    register_routers(application)
    register_health_endpoint(application)

    return application


def register_middlewares(app: FastAPI) -> None:
    """
    Register application-wide middlewares (logging, rate limit placeholder).
    """

    @app.middleware("http")
    async def logging_middleware(request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            "request completed",
            extra={
                "path": str(request.url),
                "method": request.method,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            },
        )
        return response

    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "anonymous"
        if not rate_limiter.allow(client_ip):
            return JSONResponse(
                status_code=429,
                content={
                    "status": "error",
                    "message": "Rate limit exceeded.",
                    "code": "ERR_RATE_LIMIT",
                },
            )
        return await call_next(request)


def register_health_endpoint(app: FastAPI) -> None:
    """
    Register health check endpoint.
    """

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "app": settings.app_name}


app = create_app()
