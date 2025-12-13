import sys
from pathlib import Path

import pytest

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


@pytest.fixture
def mapbox_client():
    """Create a MapboxClient instance for testing."""
    from mapbox_client import MapboxClient

    return MapboxClient()


@pytest.fixture
def sample_addresses():
    """Sample addresses for testing."""
    return [
        {
            "query": "Paris, France",
            "expected_contains": ["Paris", "France"],
        },
        {
            "query": "Amsterdam, Netherlands",
            "expected_contains": ["Amsterdam", "Netherlands"],
        },
        {
            "query": "Königstraße 57, 90762 Fuerth Germany",
            "expected_contains": ["Fürth", "Germany"],
        },
        {
            "query": "Rue Calixte Camelle 77, 33130 BEGLES France",
            "expected_contains": ["Bègles", "France"],
        },
    ]
