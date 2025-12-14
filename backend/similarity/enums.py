"""Enum for similarity method selection."""

from enum import Enum


class SimilarityMethod(str, Enum):
    """Available similarity calculation methods."""

    BASELINE = "baseline"
    LEVENSHTEIN = "levenshtein"
    JARO_WINKLER = "jaro_winkler"
    TOKEN_BASED = "token_based"
    PHONETIC = "phonetic"
    FUZZY = "fuzzy"
    GEMINI = "gemini"

    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        names = {
            self.BASELINE: "Baseline (SequenceMatcher)",
            self.LEVENSHTEIN: "Levenshtein Distance",
            self.JARO_WINKLER: "Jaro-Winkler",
            self.TOKEN_BASED: "Token-Based (Jaccard)",
            self.PHONETIC: "Phonetic (Soundex)",
            self.FUZZY: "RapidFuzz Combined",
            self.GEMINI: "Gemini (LLM)",
        }
        return names.get(self, self.value)