"""Fuzzy similarity using rapidfuzz library."""

from ..base import BaseSimilarity


class FuzzySimilarity(BaseSimilarity):
    """
    Combined fuzzy matching using rapidfuzz library.

    Combines multiple fuzzy matching algorithms:
    - Simple ratio
    - Partial ratio (for substring matching)
    - Token sort ratio
    - Token set ratio

    Falls back to pure Python implementation if rapidfuzz not available.
    """

    def __init__(self):
        self._rapidfuzz_available = False
        try:
            import rapidfuzz
            self._rapidfuzz_available = True
        except ImportError:
            pass

    @property
    def name(self) -> str:
        return "RapidFuzz Combined"

    @property
    def description(self) -> str:
        return (
            "Combines multiple fuzzy matching algorithms (ratio, partial ratio, "
            "token sort, token set) using rapidfuzz library for best overall match."
        )

    def _rapidfuzz_calculate(self, a: str, b: str) -> float:
        """Calculate similarity using rapidfuzz library."""
        from rapidfuzz import fuzz

        # Get all different similarity scores
        simple_ratio = fuzz.ratio(a, b) / 100.0
        partial_ratio = fuzz.partial_ratio(a, b) / 100.0
        token_sort = fuzz.token_sort_ratio(a, b) / 100.0
        token_set = fuzz.token_set_ratio(a, b) / 100.0

        # Weighted combination
        # Token-based methods are more important for addresses
        return (
            0.2 * simple_ratio +
            0.2 * partial_ratio +
            0.3 * token_sort +
            0.3 * token_set
        )

    def _fallback_calculate(self, a: str, b: str) -> float:
        """Fallback implementation without rapidfuzz."""
        import difflib

        # Simple ratio
        simple_ratio = difflib.SequenceMatcher(None, a, b).ratio()

        # Token sort ratio (simplified)
        tokens_a = sorted(a.split())
        tokens_b = sorted(b.split())
        sorted_a = " ".join(tokens_a)
        sorted_b = " ".join(tokens_b)
        token_sort = difflib.SequenceMatcher(None, sorted_a, sorted_b).ratio()

        # Token set ratio (simplified - intersection)
        set_a = set(tokens_a)
        set_b = set(tokens_b)
        if set_a and set_b:
            intersection = set_a & set_b
            combined_a = " ".join(sorted(intersection)) + " " + " ".join(sorted(set_a - intersection))
            combined_b = " ".join(sorted(intersection)) + " " + " ".join(sorted(set_b - intersection))
            token_set = difflib.SequenceMatcher(None, combined_a.strip(), combined_b.strip()).ratio()
        else:
            token_set = 0.0

        return 0.4 * simple_ratio + 0.3 * token_sort + 0.3 * token_set

    def calculate(self, address_a: str, address_b: str) -> float:
        if not address_a or not address_b:
            return 0.0

        a_norm = self.normalize(address_a)
        b_norm = self.normalize(address_b)

        if not a_norm or not b_norm:
            return 0.0

        if self._rapidfuzz_available:
            return self._rapidfuzz_calculate(a_norm, b_norm)
        else:
            return self._fallback_calculate(a_norm, b_norm)