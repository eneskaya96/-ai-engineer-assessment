"""Tests for Mapbox Geocoding API client."""

import pytest


class TestMapboxClient:
    """Test suite for MapboxClient."""

    def test_client_initialization(self, mapbox_client):
        """Test that client initializes with token."""
        from mapbox_client import DEFAULT_MAPBOX_BASE_URL

        assert mapbox_client.token is not None
        assert mapbox_client.base_url == DEFAULT_MAPBOX_BASE_URL

    def test_geocode_empty_query(self, mapbox_client):
        """Test that empty queries return None."""
        assert mapbox_client.geocode_best_match("") is None
        assert mapbox_client.geocode_best_match("   ") is None

    def test_geocode_simple_city(self, mapbox_client):
        """Test geocoding a simple city name."""
        result = mapbox_client.geocode_best_match("Paris, France")
        assert result is not None
        assert "Paris" in result
        assert "France" in result

    def test_geocode_dutch_address(self, mapbox_client):
        """Test geocoding a Dutch address."""
        result = mapbox_client.geocode_best_match("Amsterdam, Netherlands")
        assert result is not None
        assert "Amsterdam" in result

    def test_geocode_german_address(self, mapbox_client):
        """Test geocoding a German address with special characters."""
        result = mapbox_client.geocode_best_match("Königstraße 57, 90762 Fuerth Germany")
        assert result is not None
        assert "Germany" in result

    def test_geocode_returns_string(self, mapbox_client, sample_addresses):
        """Test that geocoding returns proper strings for various addresses."""
        for addr in sample_addresses:
            result = mapbox_client.geocode_best_match(addr["query"])
            assert result is not None, f"Failed for query: {addr['query']}"
            assert isinstance(result, str)