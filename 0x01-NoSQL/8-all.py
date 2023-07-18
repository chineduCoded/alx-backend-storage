#!/usr/bin/env python3
"""
List all documents in collection
"""
import pymongo


def list_all(mongo_collection):
    """
    function to list all doc in a collection
    """
    if mongo_collection is None:
        return []

    documents = mongo_collection.find()
    return [post for post in documents]
