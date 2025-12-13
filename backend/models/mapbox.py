from typing import List, Optional

from pydantic import BaseModel, Field


class MapboxProperties(BaseModel):
    """Properties of a Mapbox geocoding result."""
    mapbox_id: Optional[str] = None
    feature_type: Optional[str] = None
    full_address: Optional[str] = None
    name: Optional[str] = None
    name_preferred: Optional[str] = None
    place_formatted: Optional[str] = None

    def get_best_address(self) -> Optional[str]:
        """Return the best available address string."""
        if self.full_address:
            return self.full_address
        if self.name and self.place_formatted:
            return f"{self.name}, {self.place_formatted}"
        return self.name or self.place_formatted


class MapboxFeature(BaseModel):
    """A single feature from Mapbox geocoding response."""
    type: str = "Feature"
    properties: MapboxProperties


class MapboxResponse(BaseModel):
    """Mapbox Geocoding API response."""
    type: str = "FeatureCollection"
    features: List[MapboxFeature] = Field(default_factory=list)

    def get_best_match(self) -> Optional[str]:
        """Return the best matching address from the response."""
        if not self.features:
            return None
        return self.features[0].properties.get_best_address()