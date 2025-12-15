"""Cache infrastructure - Redis with in-memory fallback."""

from infrastructure.cache.client import CacheClient, cache_client

__all__ = ["CacheClient", "cache_client"]