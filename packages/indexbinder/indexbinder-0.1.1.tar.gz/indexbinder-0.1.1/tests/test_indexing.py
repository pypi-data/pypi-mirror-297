import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import faiss
import sqlite3
import json
import os
from src.indexing import BaseIndexer


class MockBlob:
    def __init__(self, name):
        self.name = name
        self._exists = False
        self._content = None

    def exists(self):
        return self._exists

    def upload_from_filename(self, filename, content_type=None):
        self._exists = True
        with open(filename, "rb") as f:
            self._content = f.read()

    def download_to_filename(self, filename):
        with open(filename, "wb") as f:
            f.write(self._content)


class MockBucket:
    def __init__(self):
        self.blobs = {}

    def blob(self, name):
        if name not in self.blobs:
            self.blobs[name] = MockBlob(name)
        return self.blobs[name]


class MockStorageClient:
    def __init__(self):
        self.buckets = {}

    def bucket(self, name):
        if name not in self.buckets:
            self.buckets[name] = MockBucket()
        return self.buckets[name]


class TestBaseIndexer(unittest.TestCase):
    @patch("src.indexing.storage.Client")
    def setUp(self, mock_storage_client):
        self.mock_storage_client = mock_storage_client
        self.mock_storage_client.return_value = MockStorageClient()
        self.indexer = BaseIndexer("test_index", "test_bucket")

    def test_add_item(self):
        # Create a temporary file
        with open("test_file.txt", "w") as f:
            f.write("Test content")

        vector = np.random.rand(512).astype("float32")
        metadata = {"key": "value"}

        self.indexer.add_item(vector, metadata, "test_file.txt")

        self.assertEqual(self.indexer.index.ntotal, 1)

        conn = sqlite3.connect(self.indexer.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM metadata WHERE id = 0")
        row = c.fetchone()
        conn.close()

        self.assertIsNotNone(row)
        self.assertEqual(json.loads(row[1]), metadata)
        self.assertEqual(row[2], "test_index/0.txt")
        self.assertEqual(row[3], "test_file.txt")
        self.assertEqual(row[4], "text/plain")

        os.remove("test_file.txt")
        os.remove(self.indexer.db_name)
        os.remove(f"{self.indexer.index_name}.index")


if __name__ == "__main__":
    unittest.main()
