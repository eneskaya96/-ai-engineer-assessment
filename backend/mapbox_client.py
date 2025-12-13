from __future__ import annotations

import os
from typing import Optional

import requests
from dotenv import load_dotenv
from pydantic import ValidationError

from models import MapboxResponse

load_dotenv()


DEFAULT_MAPBOX_BASE_URL = "https://api.mapbox.com/search/geocode/v6/forward"


class MapboxClient:
    def __init__(self, token: str | None = None, base_url: str | None = None) -> None:
        self.token = token or os.getenv("MAPBOX_ACCESS_TOKEN")
        self.base_url = base_url or os.getenv("MAPBOX_BASE_URL", DEFAULT_MAPBOX_BASE_URL)

        if not self.token:
            raise Exception("MAPBOX_ACCESS_TOKEN must be set")

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
            "limit": 1,
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            mapbox_response = MapboxResponse.model_validate(response.json())
            return mapbox_response.get_best_match()

        except ValidationError as e:
            print(f"Mapbox response validation error: {e}")
            return None
        except requests.RequestException as e:
            print(f"Mapbox API error: {e}")
            return None
