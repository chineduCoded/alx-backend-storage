#!/usr/bin/env python3
""" Cache class """
import redis
import uuid
from typing import Union

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
