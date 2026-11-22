"""Offline unit tests; run: python -m unittest discover -s tests -v"""
import unittest
from types import SimpleNamespace
from animal_shelter import AnimalShelter

class FakeCursor:
    def __init__(self, records): self.records = records
    def skip(self, n): self.records = self.records[n:]; return self
    def limit(self, n): self.records = self.records[:n]; return self
    def sort(self, fields): return self
    def __iter__(self): return iter(self.records)

class FakeCollection:
    def __init__(self): self.records = [{"id": i} for i in range(12)]; self.calls = []
    def find(self, query): self.calls.append(("find", query)); return FakeCursor(self.records[:])
    def insert_one(self, data): return SimpleNamespace(inserted_id=1)
    def update_many(self, q, values): self.calls.append(("update", q, values)); return SimpleNamespace(modified_count=1)
    def delete_many(self, q): self.calls.append(("delete", q)); return SimpleNamespace(deleted_count=1)

class FakeClient:
    def __init__(self): self.collection = FakeCollection()
    def __getitem__(self, name): return self
    def close(self): pass

class TestAnimalShelter(unittest.TestCase):
    def setUp(self):
        self.client = FakeClient()
        self.db = AnimalShelter(client=self.client)
    def test_pagination(self):
        self.assertEqual([r["id"] for r in self.db.read({}, limit=3, skip=4)], [4, 5, 6])
    def test_bounds(self):
        for limit in (0, -1, 1001, True):
            with self.assertRaises(ValueError): self.db.read({}, limit=limit)
    def test_prevent_bulk_delete(self):
        with self.assertRaises(ValueError): self.db.delete({})
        self.assertFalse(any(c[0] == "delete" for c in self.client.collection.calls))
    def test_prevent_bulk_update(self):
        with self.assertRaises(ValueError): self.db.update({}, {"name": "test"})
    def test_reject_operator_fields(self):
        with self.assertRaises(ValueError): self.db.update({"id": 1}, {"$inc": 1})
    def test_valid_write(self):
        self.assertTrue(self.db.create({"name": "test"}))
        self.assertEqual(self.db.update({"id": 1}, {"name": "test"}), 1)
        self.assertEqual(self.db.delete({"id": 1}), 1)

if __name__ == "__main__": unittest.main()
