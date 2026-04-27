from pymongo import MongoClient


class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(self, username, password):
        HOST = "localhost"
        PORT = 27017
        DB = "aac"
        COL = "animals"

        # Correct connection string with authSource
        self.client = MongoClient("mongodb://localhost:27017/")

        self.database = self.client[DB]
        self.collection = self.database[COL]

    def create(self, data):
        if data:
            self.collection.insert_one(data)
            return True
        return False

    def read(self, query):
        if query is not None:
            return list(self.collection.find(query))
        return []

    def update(self, query, new_values):
        if query is not None and new_values is not None:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.modified_count
        return 0

    def delete(self, query):
        if query is not None:
            result = self.collection.delete_many(query)
            return result.deleted_count
        return 0