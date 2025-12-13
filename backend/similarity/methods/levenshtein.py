"""Levenshtein distance based similarity."""

from similarity.base import BaseSimilarity


class LevenshteinSimilarity(BaseSimilarity):
    """
    Similarity based on Levenshtein (edit) distance.

    Calculates the minimum number of single-character edits
    (insertions, deletions, substitutions) needed to transform
    one string into another.
    """

    @property
    def name(self) -> str:
        return "Levenshtein Distance"

    @property
    def description(self) -> str:
        return (
            "Calculates edit distance (insertions, deletions, substitutions) "
            "between two strings and normalizes to [0, 1] range."
        )

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            s1, s2 = s2, s1

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Cost is 0 if characters match, 1 otherwise
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def calculate(self, address_a: str, address_b: str) -> float:
        if not address_a or not address_b:
            return 0.0

        a_norm = self.normalize(address_a)
        b_norm = self.normalize(address_b)

        if not a_norm or not b_norm:
            return 0.0

        distance = self._levenshtein_distance(a_norm, b_norm)
        max_len = max(len(a_norm), len(b_norm))

        if max_len == 0:
            return 1.0

        # Convert distance to similarity score
        return 1.0 - (distance / max_len)