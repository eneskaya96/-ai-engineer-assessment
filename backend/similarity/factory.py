"""Factory for creating similarity method instances."""

from typing import Dict, Type

from similarity.base import BaseSimilarity
from similarity.enums import SimilarityMethod
from similarity.methods import (
    BaselineSimilarity,
    LevenshteinSimilarity,
    JaroWinklerSimilarity,
    TokenBasedSimilarity,
    PhoneticSimilarity,
    FuzzySimilarity,
    GeminiSimilarity,
)


# Registry mapping enum values to classes
_METHOD_REGISTRY: Dict[SimilarityMethod, Type[BaseSimilarity]] = {
    SimilarityMethod.BASELINE: BaselineSimilarity,
    SimilarityMethod.LEVENSHTEIN: LevenshteinSimilarity,
    SimilarityMethod.JARO_WINKLER: JaroWinklerSimilarity,
    SimilarityMethod.TOKEN_BASED: TokenBasedSimilarity,
    SimilarityMethod.PHONETIC: PhoneticSimilarity,
    SimilarityMethod.FUZZY: FuzzySimilarity,
    SimilarityMethod.GEMINI: GeminiSimilarity,
}


def get_similarity_method(method: SimilarityMethod) -> BaseSimilarity:
    """
    Get a similarity method instance by enum value.

    Args:
        method: SimilarityMethod enum value

    Returns:
        Instance of the corresponding similarity class

    Raises:
        ValueError: If method is not registered
    """
    if method not in _METHOD_REGISTRY:
        raise ValueError(f"Unknown similarity method: {method}")

    return _METHOD_REGISTRY[method]()


def get_all_methods() -> Dict[SimilarityMethod, BaseSimilarity]:
    """
    Get instances of all registered similarity methods.

    Returns:
        Dictionary mapping enum values to method instances
    """
    return {method: cls() for method, cls in _METHOD_REGISTRY.items()}


def list_available_methods() -> list[dict]:
    """
    List all available similarity methods with their metadata.

    Returns:
        List of dictionaries with method info
    """
    return [
        {
            "value": method.value,
            "display_name": method.display_name,
            "description": cls().description,
        }
        for method, cls in _METHOD_REGISTRY.items()
    ]