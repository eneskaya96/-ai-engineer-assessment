"""Address service - Business logic for address operations."""

from typing import List, Optional

from domain.models import Address, PaginatedAddresses
from domain.similarity import address_similarity
from infrastructure.cache import cache_client
from infrastructure.clients import MapboxClient
from infrastructure.repositories import AddressRepository


class AddressService:
    """Service for address-related business operations."""

    CACHE_KEY_PREFIX = "address:"

    def __init__(self):
        self._mapbox_client = MapboxClient()
        self._repository = AddressRepository()
        self._cache = cache_client

    def _cache_key(self, address_id: int) -> str:
        """Generate cache key for address."""
        return f"{self.CACHE_KEY_PREFIX}{address_id}"

    def _lookup_and_score(self, address: str) -> tuple[str, float]:
        """Lookup address via Mapbox and calculate similarity score."""
        matched_address = self._mapbox_client.geocode_best_match(address)
        similarity_score = address_similarity(address, matched_address or "")
        return matched_address or "", similarity_score

    def get_all(self, page: int = 1, per_page: int = 5) -> PaginatedAddresses:
        """Get paginated addresses."""
        items, total = self._repository.get_paginated(page, per_page)
        pages = (total + per_page - 1) // per_page  # Ceiling division

        return PaginatedAddresses(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            pages=pages
        )

    def get_by_id(self, address_id: int) -> Optional[Address]:
        """Get a single address by ID with caching."""
        cache_key = self._cache_key(address_id)

        # Try cache first
        cached = self._cache.get_json(cache_key)
        if cached:
            return Address.model_validate(cached)

        # Cache miss - fetch from DB
        address = self._repository.get_by_id(address_id)
        if address:
            self._cache.set_json(cache_key, address.model_dump())

        return address

    def create(self, address: str) -> Address:
        """Create a new address with Mapbox lookup and scoring."""
        matched, score = self._lookup_and_score(address)
        return self._repository.create(address, matched, score)

    def update(self, address_id: int, new_address: str) -> Optional[Address]:
        """Update an existing address."""
        matched, score = self._lookup_and_score(new_address)
        result = self._repository.update(address_id, new_address, matched, score)

        # Invalidate cache on update
        if result:
            self._cache.delete(self._cache_key(address_id))

        return result

    def refresh(self, ids: Optional[List[int]] = None) -> None:
        """Refresh matched addresses and scores."""
        # Get addresses to refresh
        if ids:
            addresses = self._repository.get_by_ids(ids)
        else:
            addresses = self._repository.get_all()

        # Calculate new scores and batch update
        updates = []
        for addr in addresses:
            matched, score = self._lookup_and_score(addr.address)
            updates.append((addr.id, matched, score))

        self._repository.refresh_all(updates)