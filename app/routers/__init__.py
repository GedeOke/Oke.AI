
"""
Router loader for FastAPI.
"""
from fastapi import APIRouter, FastAPI


def get_api_router() -> APIRouter:
    """
    Aggregate all routers here.
    """
    router = APIRouter()
    from app.routers.auth_router import router as auth_router
    from app.routers.user_router import router as user_router
    from app.routers.organization_router import router as organization_router
    from app.routers.customer_router import router as customer_router
    from app.routers.conversation_router import router as conversation_router
    from app.routers.message_router import router as message_router

    router.include_router(auth_router)
    router.include_router(user_router)
    router.include_router(organization_router)
    router.include_router(customer_router)
    router.include_router(conversation_router)
    router.include_router(message_router)
    return router


def register_routers(app: FastAPI) -> None:
    """
    Register routers with the FastAPI application.
    """
    app.include_router(get_api_router())
