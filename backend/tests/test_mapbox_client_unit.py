"""Unit tests for Mapbox Geocoding API client with mocked responses."""

import pytest
import requests


class TestMapboxClientUnit:
    """Unit test suite with mocked API responses."""

    def test_geocode_api_error_handling(self, mapbox_client, mocker):
        """Test that API errors are handled gracefully."""
        mocker.patch(
            "infrastructure.clients.mapbox.client.requests.get",
            side_effect=requests.RequestException("Network error"),
        )

        result = mapbox_client.geocode_best_match("Test Address")
        assert result is None

    def test_geocode_empty_response(self, mapbox_client, mocker):
        """Test handling of empty API response."""
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"features": []}
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch("infrastructure.clients.mapbox.client.requests.get", return_value=mock_response)

        result = mapbox_client.geocode_best_match("Nonexistent Place XYZ123")
        assert result is None

    def test_geocode_successful_response(self, mapbox_client, mocker):
        """Test successful API response parsing."""
        mock_response = mocker.Mock()
        mock_response.json.return_value = {
            "features": [
                {
                    "properties": {
                        "full_address": "123 Test Street, Test City, Country",
                        "name": "123 Test Street",
                        "place_formatted": "Test City, Country",
                    }
                }
            ]
        }
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch("infrastructure.clients.mapbox.client.requests.get", return_value=mock_response)

        result = mapbox_client.geocode_best_match("Test Address")
        assert result == "123 Test Street, Test City, Country"

    def test_geocode_fallback_to_name_and_place(self, mapbox_client, mocker):
        """Test fallback when full_address is not available."""
        mock_response = mocker.Mock()
        mock_response.json.return_value = {
            "features": [
                {
                    "properties": {
                        "name": "Test Location",
                        "place_formatted": "Test City, Country",
                    }
                }
            ]
        }
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch("infrastructure.clients.mapbox.client.requests.get", return_value=mock_response)

        result = mapbox_client.geocode_best_match("Test Address")
        assert result == "Test Location, Test City, Country"