"""
Customer endpoints.
"""
from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.db.supabase import get_supabase_client
from app.schemas.customer_schema import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services import customer_service

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=list[CustomerResponse])
def list_customers(client=Depends(get_supabase_client), current_user=Depends(get_current_user)):
    return customer_service.list_customers(current_user["organization_id"], client)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str, client=Depends(get_supabase_client), current_user=Depends(get_current_user)):
    return customer_service.get_customer(current_user["organization_id"], customer_id, client)


@router.post("", response_model=CustomerResponse)
def create_customer(payload: CustomerCreate, client=Depends(get_supabase_client), current_user=Depends(get_current_user)):
    return customer_service.create_customer(current_user["organization_id"], payload, client)


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: str,
    payload: CustomerUpdate,
    client=Depends(get_supabase_client),
    current_user=Depends(get_current_user),
):
    return customer_service.update_customer(current_user["organization_id"], customer_id, payload, client)


@router.delete("/{customer_id}")
def delete_customer(customer_id: str, client=Depends(get_supabase_client), current_user=Depends(get_current_user)):
    return customer_service.delete_customer(current_user["organization_id"], customer_id, client)
