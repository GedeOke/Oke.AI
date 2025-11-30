
"""
Router loader for FastAPI.
"""
from fastapi import APIRouter, FastAPI


def get_api_router() -> APIRouter:
    """
    Aggregate all routers here.
    """
    router = APIRouter()
    return router


def register_routers(app: FastAPI) -> None:
    """
    Register routers with the FastAPI application.
    """
    app.include_router(get_api_router())
