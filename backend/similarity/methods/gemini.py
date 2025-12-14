"""Gemini-based similarity using Google's Generative AI."""

import os
from similarity.base import BaseSimilarity


DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


class GeminiSimilarity(BaseSimilarity):
    """
    LLM-based similarity using Google Gemini.

    Sends both addresses to Gemini and asks for a similarity score.
    Leverages semantic understanding for better handling of:
    - Language differences (Parijs vs Paris)
    - Abbreviations and formatting
    - Missing/extra information
    """

    def __init__(self):
        self._client = None
        self._model_name = None
        self._available = False
        self._init_client()

    def _init_client(self):
        """Initialize Gemini client if API key is available."""
        try:
            from google import genai

            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                self._client = genai.Client(api_key=api_key)
                self._model_name = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
                self._available = True
                print(f"Gemini initialized with model: {self._model_name}")
            else:
                print("Gemini: GEMINI_API_KEY not found in environment")
        except ImportError as e:
            print(f"Gemini: Import error - {e}")
        except Exception as e:
            print(f"Gemini: Init error - {type(e).__name__}: {e}")

    @property
    def name(self) -> str:
        return "Gemini (LLM)"

    @property
    def description(self) -> str:
        return (
            "Uses Google Gemini LLM to semantically compare addresses. "
            "Handles language differences, abbreviations, and formatting variations."
        )

    def calculate(self, address_a: str, address_b: str) -> float:
        if not address_a or not address_b:
            return 0.0

        if not self._available:
            return 0.5

        prompt = f"""Compare these two addresses and return ONLY a similarity score between 0.0 and 1.0.

Address 1: {address_a}
Address 2: {address_b}

Scoring guide:
- 1.0: Same location (even if different languages/formats)
- 0.7-0.9: Very likely same location, minor differences
- 0.4-0.6: Same city/region but different street
- 0.1-0.3: Same country but different city
- 0.0: Completely different locations

Return ONLY the number, nothing else."""

        try:
            response = self._client.models.generate_content(
                model=self._model_name,
                contents=prompt
            )
            score_text = response.text.strip()
            score = float(score_text)
            return max(0.0, min(1.0, score))
        except Exception as e:
            print(f"Gemini API error: {type(e).__name__}: {e}")
            return 0.5