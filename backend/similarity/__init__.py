"""Similarity module for address matching."""

from similarity.base import BaseSimilarity
from similarity.enums import SimilarityMethod
from similarity.factory import (
    get_similarity_method,
    get_all_methods,
    list_available_methods,
)
from similarity.methods import (
    BaselineSimilarity,
    LevenshteinSimilarity,
    JaroWinklerSimilarity,
    TokenBasedSimilarity,
    PhoneticSimilarity,
    FuzzySimilarity,
)

__all__ = [
    # Base class
    "BaseSimilarity",
    # Enum
    "SimilarityMethod",
    # Factory functions
    "get_similarity_method",
    "get_all_methods",
    "list_available_methods",
    # Method classes
    "BaselineSimilarity",
    "LevenshteinSimilarity",
    "JaroWinklerSimilarity",
    "TokenBasedSimilarity",
    "PhoneticSimilarity",
    "FuzzySimilarity",
]