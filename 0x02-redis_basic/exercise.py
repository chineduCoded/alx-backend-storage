#!/usr/bin/env python3
""" Cache class """
import redis
import uuid
from typing import Union, Callable

UnionOfTypes = Union[str, bytes, int, float]


class Cache:
    """Represent Cache System"""
    def __init__(self):
        """Connect redis and store the client instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: UnionOfTypes) -> str:
        """Generate a random key using uuid"""
        self._key = str(uuid.uuid4())

        self._redis.set(self._key, data)

        return self._key

    def get(self, key: str, fn: Callable = None) -> UnionOfTypes:
        """Get stored cache"""
        value = self._redis.get(key)
        if value is None:
            return None

        if fn is not None:
            return fn(value)

        return value

    def get_str(self, key: str) -> str:
        """Get stored value as string"""
        return self.get(key, fn=lambda x: x.decode())

    def get_int(self, key: str) -> int:
        """Get stored cached as int"""
        return self.get(key, fn=int)
