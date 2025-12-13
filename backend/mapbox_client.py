from __future__ import annotations

import os
from typing import Optional

import requests
from dotenv import load_dotenv
from pydantic import ValidationError

from models import MapboxResponse

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
