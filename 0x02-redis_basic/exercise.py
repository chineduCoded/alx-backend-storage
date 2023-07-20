#!/usr/bin/env python3
""" Cache class """
import redis
import uuid
import functools
from typing import Union, Callable

UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    count how many times methods of the Cache class are called
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrap the decorated function and return the wrapper"""
        input_key = f"{method.__qualname__}:inputs"
        self._redis.rpush(input_key, str(args))

        output = str(method(self, *args, **kwargs))

        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(output_key, output)

        return output

    return wrapper


class Cache:
    """Represent Cache System"""
    def __init__(self):
        """Connect redis and store the client instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
