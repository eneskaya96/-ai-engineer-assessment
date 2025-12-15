"""Address repository - Data access layer."""

from typing import List, Optional, Sequence

from sqlalchemy import select, func

from domain.models import Address
from infrastructure.database import db
from infrastructure.entities import AddressEntity


class AddressRepository:
    """Repository for address data access operations."""

    def get_all(self) -> List[Address]:
        """Get all addresses."""
        with db.session() as session:
            entities: Sequence[AddressEntity] = session.scalars(
                select(AddressEntity)
            ).all()
            return [entity.to_domain() for entity in entities]

    def get_paginated(self, page: int = 1, per_page: int = 20) -> tuple[List[Address], int]:
        """Get paginated addresses with total count."""
        with db.session() as session:
            # Get total count
            total = session.scalar(select(func.count(AddressEntity.id)))

            # Get paginated results
            offset = (page - 1) * per_page
            entities: Sequence[AddressEntity] = session.scalars(
                select(AddressEntity)
                .order_by(AddressEntity.id.desc())
                .offset(offset)
                .limit(per_page)
            ).all()

            return [entity.to_domain() for entity in entities], total

    def get_by_id(self, address_id: int) -> Optional[Address]:
        """Get address by ID."""
        with db.session() as session:
            entity = session.scalars(
                select(AddressEntity).where(AddressEntity.id == address_id)
            ).one_or_none()
            return entity.to_domain() if entity else None

    def get_by_ids(self, ids: List[int]) -> List[Address]:
        """Get addresses by list of IDs."""
        with db.session() as session:
            entities: Sequence[AddressEntity] = session.scalars(
                select(AddressEntity).where(AddressEntity.id.in_(ids))
            ).all()
            return [entity.to_domain() for entity in entities]

    def create(self, address: str, matched_address: str, match_score: float) -> Address:
        """Create a new address."""
        with db.session() as session:
            entity = AddressEntity(
                address=address,
                matched_address=matched_address,
                match_score=match_score
            )
            session.add(entity)
            session.flush()
            return entity.to_domain()

    def update(
        self,
        address_id: int,
        address: str,
        matched_address: str,
        match_score: float
    ) -> Optional[Address]:
        """Update an existing address."""
        with db.session() as session:
            entity = session.scalars(
                select(AddressEntity).where(AddressEntity.id == address_id)
            ).one_or_none()

            if not entity:
                return None

            entity.address = address
            entity.matched_address = matched_address
            entity.match_score = match_score
            session.flush()
            return entity.to_domain()

    def update_match(
        self,
        address_id: int,
        matched_address: str,
        match_score: float
    ) -> None:
        """Update only the match data for an address."""
        with db.session() as session:
            entity = session.scalars(
                select(AddressEntity).where(AddressEntity.id == address_id)
            ).one_or_none()

            if entity:
                entity.matched_address = matched_address
                entity.match_score = match_score

    def refresh_all(self, updates: List[tuple[int, str, float]]) -> None:
        """Batch update match data for multiple addresses."""
        with db.session() as session:
            for address_id, matched_address, match_score in updates:
                entity = session.scalars(
                    select(AddressEntity).where(AddressEntity.id == address_id)
                ).one_or_none()

                if entity:
                    entity.matched_address = matched_address
                    entity.match_score = match_score