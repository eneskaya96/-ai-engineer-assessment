"""Quick test for a single address pair with a specific method."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from similarity import SimilarityMethod, get_similarity_method


# ============ CONFIGURE HERE ============
METHOD = SimilarityMethod.GEMINI
ADDRESS_A = "Parijs, Frankrijk"
ADDRESS_B = "Paris, France"
# ========================================


def test_single_method():
    """Test a single method with configured addresses."""
    method = get_similarity_method(METHOD)

    print(f"\nMethod: {method.name}")
    print(f"Address A: {ADDRESS_A}")
    print(f"Address B: {ADDRESS_B}")

    score = method.calculate(ADDRESS_A, ADDRESS_B)
    print(f"Score: {score}")

    assert 0.0 <= score <= 1.0