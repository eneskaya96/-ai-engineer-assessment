"""Baseline similarity using Python's difflib SequenceMatcher."""

import difflib

from similarity.base import BaseSimilarity


class BaselineSimilarity(BaseSimilarity):
    """
    Baseline similarity using difflib.SequenceMatcher.

    Uses longest contiguous matching subsequence algorithm.
    Simple but effective for basic string comparison.
    """

    @property
    def name(self) -> str:
        return "Baseline (SequenceMatcher)"

    @property
    def description(self) -> str:
        return (
            "Uses Python's difflib.SequenceMatcher which finds the longest "
            "contiguous matching subsequence. Simple character-level comparison."
        )

    def calculate(self, address_a: str, address_b: str) -> float:
        if not address_a or not address_b:
            return 0.0

        a_norm = self.normalize(address_a)
        b_norm = self.normalize(address_b)

        if not a_norm or not b_norm:
            return 0.0

        return difflib.SequenceMatcher(None, a_norm, b_norm).ratio()