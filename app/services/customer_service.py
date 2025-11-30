"""
Customer service logic with org scoping.
"""
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import HTTPException, status
from supabase import Client

from app.schemas.customer_schema import CustomerCreate, CustomerResponse, CustomerUpdate
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _map_customer(data: Dict) -> CustomerResponse:
    return CustomerResponse(
        id=data["id"],
        organization_id=data["organization_id"],
        external_id=data.get("external_id"),
        name=data.get("name"),
        phone=data.get("phone"),
        email=data.get("email"),
        source=data.get("source"),
        created_at=data.get("created_at"),
    )


def list_customers(org_id: str, client: Client) -> List[CustomerResponse]:
    result = client.table("customers").select("*").eq("organization_id", org_id).execute()
    data = getattr(result, "data", None) or []
    return [_map_customer(item) for item in data]


def get_customer(org_id: str, customer_id: str, client: Client) -> CustomerResponse:
    result = (
        client.table("customers")
        .select("*")
        .eq("organization_id", org_id)
        .eq("id", customer_id)
        .limit(1)
        .execute()
    )
    data = getattr(result, "data", None) or []
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )
    return _map_customer(data[0])


def create_customer(org_id: str, payload: CustomerCreate, client: Client) -> CustomerResponse:
    record = {
        "id": str(uuid4()),
        "organization_id": org_id,
        "external_id": payload.external_id,
        "name": payload.name,
        "phone": payload.phone,
        "email": payload.email,
        "source": payload.source,
    }
    try:
        result = client.table("customers").insert(record).execute()
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Failed to create customer")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create customer.",
        ) from exc
    data = getattr(result, "data", None) or [record]
    return _map_customer(data[0])


def update_customer(org_id: str, customer_id: str, payload: CustomerUpdate, client: Client) -> CustomerResponse:
    updates = {k: v for k, v in payload.dict().items() if v is not None}
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update.",
        )
    try:
        result = (
            client.table("customers")
            .update(updates)
            .eq("organization_id", org_id)
            .eq("id", customer_id)
            .execute()
        )
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Failed to update customer")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update customer.",
        ) from exc
    data = getattr(result, "data", None) or []
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )
    return _map_customer(data[0])


def delete_customer(org_id: str, customer_id: str, client: Client) -> Dict[str, str]:
    try:
        client.table("customers").delete().eq("organization_id", org_id).eq("id", customer_id).execute()
    except Exception as exc:  # pragma: no cover - external service
        logger.exception("Failed to delete customer")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete customer.",
        ) from exc
    return {"message": "Customer deleted"}


def find_or_create_customer(org_id: str, external_id: str, source: str, client: Client) -> CustomerResponse:
    result = (
        client.table("customers")
        .select("*")
        .eq("organization_id", org_id)
        .eq("external_id", external_id)
        .eq("source", source)
        .limit(1)
        .execute()
    )
    data = getattr(result, "data", None) or []
    if data:
        return _map_customer(data[0])
    return create_customer(
        org_id,
        CustomerCreate(external_id=external_id, source=source),
        client,
    )
