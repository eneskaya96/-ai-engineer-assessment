"""Address ORM entity."""

from sqlalchemy import Column, Integer, String, Float

from domain.models import Address
from infrastructure.database import Base


class AddressEntity(Base):
    """ORM entity for addresses table."""
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    matched_address = Column(String, nullable=True)
    match_score = Column(Float, nullable=True)

    def to_domain(self) -> Address:
        """Convert ORM entity to domain model."""
        return Address(
            id=self.id,
            address=self.address,
            matched_address=self.matched_address,
            match_score=self.match_score
        )