"""Address domain models."""

from typing import List, Optional

from pydantic import BaseModel


class Address(BaseModel):
    """Address entity returned from API."""
    id: int
    address: str
    matched_address: Optional[str]
    match_score: float


class AddressCreate(BaseModel):
    """Schema for creating a new address."""
    address: str


class AddressUpdate(BaseModel):
    """Schema for updating an existing address."""
    address: str


class AddressesRefresh(BaseModel):
    """Schema for refreshing addresses."""
    ids: List[int] | None


class PaginatedAddresses(BaseModel):
    """Paginated response for addresses."""
    items: List[Address]
    total: int
    page: int
    per_page: int
    pages: int