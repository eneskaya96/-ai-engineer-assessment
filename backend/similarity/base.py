"""Abstract base class for similarity methods."""

from abc import ABC, abstractmethod


class BaseSimilarity(ABC):
    """Abstract base class for address similarity calculations."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the similarity method."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of how this method works."""
        pass

    def normalize(self, text: str) -> str:
        """Basic text normalization. Can be overridden by subclasses."""
        if not text:
            return ""
        return " ".join(text.strip().lower().split())

    @abstractmethod
    def calculate(self, address_a: str, address_b: str) -> float:
        """
        Calculate similarity between two addresses.

        Args:
            address_a: First address string
            address_b: Second address string

        Returns:
            Similarity score between 0.0 and 1.0
            1.0 = identical/same location
            0.0 = completely different
        """
        pass

    def __call__(self, address_a: str, address_b: str) -> float:
        """Allow instance to be called as a function."""
        return self.calculate(address_a, address_b)