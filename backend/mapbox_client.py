from __future__ import annotations

import os
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()


class MapboxClient:
    def __init__(self, token: str | None = None) -> None:
        self.token = token or os.getenv("MAPBOX_ACCESS_TOKEN")

        if not self.token:
            raise Exception("MAPBOX_ACCESS_TOKEN must be set")

        self.base_url = "https://api.mapbox.com/search/geocode/v6/forward"

    def geocode_best_match(self, query: str) -> Optional[str]:
        """
        Find the best matching address for a given query using Mapbox Geocoding API.

        Returns the full_address of the best match, or None if no match found.
        """
        if not query or not query.strip():
            return None

        params = {
            "q": query,
            "access_token": self.token,
            "limit": 1,  # Only get the best match
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            features = data.get("features", [])
            if not features:
                return None

            # Get the best match (first result)
            best_match = features[0]
            properties = best_match.get("properties", {})

            # Return full_address if available, otherwise construct from name + place_formatted
            full_address = properties.get("full_address")
            if full_address:
                return full_address

            # Fallback: use name and place_formatted
            name = properties.get("name", "")
            place_formatted = properties.get("place_formatted", "")
            if name and place_formatted:
                return f"{name}, {place_formatted}"

            return name or place_formatted or None

        except requests.RequestException as e:
            print(f"Mapbox API error: {e}")
            return None
