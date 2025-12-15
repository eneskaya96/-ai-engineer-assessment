"""Address API endpoints."""

from fastapi import APIRouter, Query

from config import settings
from domain.models import (
    Address,
    AddressCreate,
    AddressUpdate,
    AddressesRefresh,
    PaginatedAddresses,
)
from application.services.address_service import AddressService

router = APIRouter(prefix="/addresses", tags=["addresses"])

address_service = AddressService()


@router.get("", response_model=PaginatedAddresses)
def get_addresses(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(
        default=settings.default_page_size,
        ge=1,
        le=settings.max_page_size,
        description="Items per page"
    ),
) -> PaginatedAddresses:
    """Get paginated addresses."""
    return address_service.get_all(page=page, per_page=per_page)


@router.get("/{address_id}", response_model=Address)
def get_address(address_id: int) -> Address:
    """Get a single address by ID."""
    return address_service.get_by_id(address_id)


@router.post("", response_model=Address, status_code=201)
def create_address(payload: AddressCreate) -> Address:
    """Create a new address with Mapbox lookup and similarity scoring."""
    return address_service.create(payload.address)


@router.post("/{address_id}", response_model=Address, status_code=201)
def update_address(address_id: int, payload: AddressUpdate) -> Address:
    """Update an existing address."""
    return address_service.update(address_id, payload.address)


@router.post("/refresh", status_code=200)
def refresh_addresses(payload: AddressesRefresh):
    """Refresh matched addresses and scores for selected or all addresses."""
    address_service.refresh(payload.ids)