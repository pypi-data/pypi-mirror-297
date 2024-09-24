import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoDBClient(MongoClient):
    instance: MongoClient = None

    def __new__(cls, uri: str) -> MongoClient:
        if not hasattr(cls, 'instance') or cls.instance is None:
            cls.instance = MongoClient(uri, server_api=ServerApi('1'))
        return cls.instance
