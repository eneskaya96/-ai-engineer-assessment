"""Cache client with Redis and in-memory fallback."""

import json
import time
from typing import Any, Optional

from config import settings


class InMemoryCache:
    """Simple in-memory cache with TTL support."""

    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[str]:
        """Get value from cache if not expired."""
        if key not in self._store:
            return None

        value, expires_at = self._store[key]
        if time.time() > expires_at:
            del self._store[key]
            return None

        return value

    def set(self, key: str, value: str, ttl: int) -> None:
        """Set value with TTL in seconds."""
        expires_at = time.time() + ttl
        self._store[key] = (value, expires_at)

    def delete(self, key: str) -> None:
        """Delete key from cache."""
        self._store.pop(key, None)


class CacheClient:
    """Cache client that uses Redis if available, otherwise in-memory."""

    def __init__(self):
        self._redis = None
        self._memory_cache = None

        if settings.redis_url:
            try:
                import redis
                self._redis = redis.from_url(settings.redis_url)
                self._redis.ping()  # Test connection
            except Exception:
                self._redis = None

        if self._redis is None:
            self._memory_cache = InMemoryCache()

    @property
    def is_redis(self) -> bool:
        """Check if using Redis backend."""
        return self._redis is not None

    def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        if self._redis:
            value = self._redis.get(key)
            return value.decode() if value else None
        return self._memory_cache.get(key)

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        """Set value with optional TTL."""
        ttl = ttl or settings.cache_ttl
        if self._redis:
            self._redis.setex(key, ttl, value)
        else:
            self._memory_cache.set(key, value, ttl)

    def delete(self, key: str) -> None:
        """Delete key from cache."""
        if self._redis:
            self._redis.delete(key)
        else:
            self._memory_cache.delete(key)

    def get_json(self, key: str) -> Optional[dict]:
        """Get and deserialize JSON value."""
        value = self.get(key)
        if value:
            return json.loads(value)
        return None

    def set_json(self, key: str, value: dict, ttl: Optional[int] = None) -> None:
        """Serialize and set JSON value."""
        self.set(key, json.dumps(value), ttl)


# Singleton instance
cache_client = CacheClient()