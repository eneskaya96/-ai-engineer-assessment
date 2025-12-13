"""
Address similarity module.

This module provides the main entry point for address similarity calculation.
The actual implementations are in the similarity/ package.
"""

from similarity import SimilarityMethod, get_similarity_method

# Default method to use (Jaro-Winkler has best MAE: 0.1387)
DEFAULT_METHOD = SimilarityMethod.JARO_WINKLER

# Cached instance of the default method
_default_instance = None


def _get_default_instance():
    """Get or create the default similarity method instance."""
    global _default_instance
    if _default_instance is None:
        _default_instance = get_similarity_method(DEFAULT_METHOD)
    return _default_instance


def address_similarity(a: str, b: str, method: SimilarityMethod | None = None) -> float:
    """
    Calculate similarity between two addresses.

    Args:
        a: First address string
        b: Second address string
        method: Optional similarity method to use. If None, uses DEFAULT_METHOD.

    Returns:
        Similarity score between 0.0 and 1.0
        1.0 = identical/same location
        0.0 = completely different
    """
    if not a or not b:
        return 0.0

    if method is not None:
        instance = get_similarity_method(method)
        return instance.calculate(a, b)

    return _get_default_instance().calculate(a, b)


def baseline_similarity(a: str, b: str) -> float:
    """
    Legacy baseline similarity function.

    Kept for backwards compatibility.
    Uses the baseline SequenceMatcher method.
    """
    instance = get_similarity_method(SimilarityMethod.BASELINE)
    return instance.calculate(a, b)