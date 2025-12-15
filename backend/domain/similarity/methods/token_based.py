"""Token-based similarity methods."""

import re
from typing import Set

from ..base import BaseSimilarity


class TokenBasedSimilarity(BaseSimilarity):
    """
    Token-based similarity using Jaccard index and token matching.

    Splits addresses into tokens (words) and compares the overlap.
    More robust to word reordering than character-based methods.
    """

    @property
    def name(self) -> str:
        return "Token-Based (Jaccard)"

    @property
    def description(self) -> str:
        return (
            "Splits addresses into tokens and calculates Jaccard similarity "
            "(intersection over union). Robust to word reordering."
        )

    def _tokenize(self, text: str) -> Set[str]:
        """Split text into normalized tokens."""
        normalized = self.normalize(text)
        # Split on non-alphanumeric characters
        tokens = re.split(r'[^a-z0-9]+', normalized)
        # Filter empty tokens and very short ones (likely noise)
        return {t for t in tokens if len(t) > 1}

    def _jaccard_similarity(self, set1: Set[str], set2: Set[str]) -> float:
        """Calculate Jaccard similarity between two sets."""
        if not set1 or not set2:
            return 0.0

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        if union == 0:
            return 0.0

        return intersection / union

    def _token_sort_ratio(self, tokens1: Set[str], tokens2: Set[str]) -> float:
        """
        Sort tokens alphabetically and compare.
        Helps with different orderings of the same components.
        """
        sorted1 = " ".join(sorted(tokens1))
        sorted2 = " ".join(sorted(tokens2))

        if not sorted1 or not sorted2:
            return 0.0

        # Use simple ratio on sorted strings
        import difflib
        return difflib.SequenceMatcher(None, sorted1, sorted2).ratio()

    def calculate(self, address_a: str, address_b: str) -> float:
        if not address_a or not address_b:
            return 0.0

        tokens_a = self._tokenize(address_a)
        tokens_b = self._tokenize(address_b)

        if not tokens_a or not tokens_b:
            return 0.0

        # Combine Jaccard and token sort ratio
        jaccard = self._jaccard_similarity(tokens_a, tokens_b)
        token_sort = self._token_sort_ratio(tokens_a, tokens_b)

        # Weighted combination (Jaccard is more important for addresses)
        return 0.6 * jaccard + 0.4 * token_sort