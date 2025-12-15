"""Phonetic similarity using Soundex algorithm."""

import re
from typing import Set

from ..base import BaseSimilarity


class PhoneticSimilarity(BaseSimilarity):
    """
    Phonetic similarity using Soundex algorithm.

    Encodes words by their sound, helping match addresses
    with spelling variations or transliterations.
    E.g., "Parijs" and "Paris" would have similar Soundex codes.
    """

    @property
    def name(self) -> str:
        return "Phonetic (Soundex)"

    @property
    def description(self) -> str:
        return (
            "Uses Soundex phonetic encoding to match addresses by sound. "
            "Helps with spelling variations and transliterations across languages."
        )

    def _soundex(self, word: str) -> str:
        """
        Generate Soundex code for a word.

        Soundex encoding rules:
        - Keep first letter
        - Replace consonants with digits
        - Remove vowels, H, W, Y
        - Remove consecutive duplicates
        - Pad or truncate to 4 characters
        """
        if not word:
            return ""

        word = word.upper()

        # Mapping of letters to Soundex codes
        mapping = {
            'B': '1', 'F': '1', 'P': '1', 'V': '1',
            'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
            'D': '3', 'T': '3',
            'L': '4',
            'M': '5', 'N': '5',
            'R': '6',
        }

        # Keep first letter
        first_letter = word[0]
        coded = first_letter

        # Encode rest of the word
        prev_code = mapping.get(first_letter, '')
        for char in word[1:]:
            code = mapping.get(char, '')
            if code and code != prev_code:
                coded += code
            prev_code = code if code else prev_code

        # Pad or truncate to 4 characters
        coded = coded[:4].ljust(4, '0')

        return coded

    def _tokenize(self, text: str) -> Set[str]:
        """Extract alphabetic tokens from text."""
        normalized = self.normalize(text)
        tokens = re.findall(r'[a-z]+', normalized)
        # Only consider meaningful tokens
        return {t for t in tokens if len(t) > 2}

    def calculate(self, address_a: str, address_b: str) -> float:
        if not address_a or not address_b:
            return 0.0

        tokens_a = self._tokenize(address_a)
        tokens_b = self._tokenize(address_b)

        if not tokens_a or not tokens_b:
            return 0.0

        # Generate Soundex codes for all tokens
        codes_a = {self._soundex(t) for t in tokens_a}
        codes_b = {self._soundex(t) for t in tokens_b}

        # Calculate Jaccard similarity on Soundex codes
        intersection = len(codes_a & codes_b)
        union = len(codes_a | codes_b)

        if union == 0:
            return 0.0

        phonetic_score = intersection / union

        # Also factor in token overlap for numbers and short codes
        # (Soundex doesn't handle numbers well)
        numeric_a = {t for t in tokens_a if t.isdigit()}
        numeric_b = {t for t in tokens_b if t.isdigit()}

        if numeric_a and numeric_b:
            numeric_intersection = len(numeric_a & numeric_b)
            numeric_union = len(numeric_a | numeric_b)
            numeric_score = numeric_intersection / numeric_union if numeric_union > 0 else 0
            # Combine phonetic and numeric scores
            return 0.7 * phonetic_score + 0.3 * numeric_score

        return phonetic_score