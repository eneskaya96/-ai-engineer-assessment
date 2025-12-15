"""Jaro-Winkler similarity algorithm."""

from ..base import BaseSimilarity


class JaroWinklerSimilarity(BaseSimilarity):
    """
    Jaro-Winkler similarity algorithm.

    Originally designed for name matching, gives higher weight
    to strings that match from the beginning (common prefix bonus).
    Good for addresses where street names often share prefixes.
    """

    def __init__(self, winkler_prefix_weight: float = 0.1):
        """
        Initialize Jaro-Winkler similarity.

        Args:
            winkler_prefix_weight: Weight for common prefix bonus (default 0.1)
        """
        self.winkler_prefix_weight = winkler_prefix_weight

    @property
    def name(self) -> str:
        return "Jaro-Winkler"

    @property
    def description(self) -> str:
        return (
            "Jaro-Winkler algorithm with prefix bonus. Originally designed for "
            "name matching, effective for addresses sharing common prefixes."
        )

    def _jaro_similarity(self, s1: str, s2: str) -> float:
        """Calculate Jaro similarity between two strings."""
        if s1 == s2:
            return 1.0

        len1, len2 = len(s1), len(s2)
        if len1 == 0 or len2 == 0:
            return 0.0

        # Maximum distance for matching characters
        match_distance = max(len1, len2) // 2 - 1
        if match_distance < 0:
            match_distance = 0

        s1_matches = [False] * len1
        s2_matches = [False] * len2

        matches = 0
        transpositions = 0

        # Find matches
        for i in range(len1):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len2)

            for j in range(start, end):
                if s2_matches[j] or s1[i] != s2[j]:
                    continue
                s1_matches[i] = True
                s2_matches[j] = True
                matches += 1
                break

        if matches == 0:
            return 0.0

        # Count transpositions
        k = 0
        for i in range(len1):
            if not s1_matches[i]:
                continue
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1

        transpositions //= 2

        return (
            matches / len1 + matches / len2 + (matches - transpositions) / matches
        ) / 3.0

    def calculate(self, address_a: str, address_b: str) -> float:
        if not address_a or not address_b:
            return 0.0

        a_norm = self.normalize(address_a)
        b_norm = self.normalize(address_b)

        if not a_norm or not b_norm:
            return 0.0

        jaro = self._jaro_similarity(a_norm, b_norm)

        # Calculate common prefix length (max 4 chars)
        prefix_len = 0
        for i in range(min(len(a_norm), len(b_norm), 4)):
            if a_norm[i] == b_norm[i]:
                prefix_len += 1
            else:
                break

        # Apply Winkler modification
        return jaro + prefix_len * self.winkler_prefix_weight * (1 - jaro)