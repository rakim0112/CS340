"""Enhanced MongoDB CRUD layer for the CS-499 database artifact.

Original coursework remains on main; this branch adds defensive validation and
bounded reads. Requires pymongo and a locally accessible authorized MongoDB.
"""
from collections.abc import Mapping
from pymongo import MongoClient

class AnimalShelter:
    def __init__(self, username=None, password=None, *, uri="mongodb://localhost:27017/",
                 database="aac", collection="animals", client=None, auth_source=None):
        if (username is None) != (password is None):
            raise ValueError("Provide both username and password, or neither")
        if client is None:
            options = {"serverSelectionTimeoutMS": 5000}
            if username is not None:
                options.update(username=username, password=password)
                if auth_source:
                    options["authSource"] = auth_source
            client = MongoClient(uri, **options)
        self.client = client
        self.database = client[database]
        self.collection = self.database[collection]

    @staticmethod
    def _mapping(value, name, *, nonempty=False):
        if not isinstance(value, Mapping) or (nonempty and not value):
            raise ValueError(f"{name} must be a {'non-empty ' if nonempty else ''}mapping")
        return dict(value)

    def create(self, data):
        document = self._mapping(data, "data", nonempty=True)
        result = self.collection.insert_one(document)
        return result.inserted_id is not None

    def read(self, query=None, *, limit=100, skip=0, sort=None):
        query = self._mapping({} if query is None else query, "query")
        if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 1000:
            raise ValueError("limit must be an integer between 1 and 1000")
        if not isinstance(skip, int) or isinstance(skip, bool) or skip < 0:
            raise ValueError("skip must be a nonnegative integer")
        cursor = self.collection.find(query).skip(skip).limit(limit)
        if sort is not None:
            if not isinstance(sort, list):
                raise ValueError("sort must be a list of (field, direction) pairs")
            cursor = cursor.sort(sort)
        return list(cursor)

    def update(self, query, new_values):
        query = self._mapping(query, "query", nonempty=True)
        values = self._mapping(new_values, "new_values", nonempty=True)
        if any(str(key).startswith("$") or "." in str(key) for key in values):
            raise ValueError("Replacement fields cannot contain operators or dotted paths")
        result = self.collection.update_many(query, {"$set": values})
        return result.modified_count

    def delete(self, query):
        query = self._mapping(query, "query", nonempty=True)
        return self.collection.delete_many(query).deleted_count

    def close(self):
        self.client.close()

# Backward-compatible alias for code using the original class name.
AnimalShelterLegacy = AnimalShelter
