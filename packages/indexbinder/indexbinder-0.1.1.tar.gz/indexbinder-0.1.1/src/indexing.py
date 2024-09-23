import hashlib
import faiss
import numpy as np
import sqlite3
from google.cloud import storage
import google.api_core.exceptions
import google.auth.exceptions
import os
import json
import mimetypes
import logging
import sys
import base64

stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [stdout_handler]

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=handlers,
)
logger = logging.getLogger(__name__)


class BaseIndexer:
    def __init__(
        self, index_name, gcs_project, bucket_name, vector_size, check_consistency=False
    ):
        self.index_name = index_name
        self.bucket_name = bucket_name
        self.index = faiss.IndexFlatIP(vector_size)
        self.db_name = f"{index_name}.sqlite"
        self.gcs_client = storage.Client(project=gcs_project)
        self.bucket = self.gcs_client.bucket(bucket_name)
        self.check_consistency = check_consistency

        logger.info(
            f"Initializing BaseIndexer with index_name: {index_name}, bucket_name: {bucket_name}"
        )
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.setup_database()
        self.load_index()

    def setup_database(self):
        logger.info(f"Setting up database: {self.db_name}")
        c = self.conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS embeddings
                     (id INTEGER PRIMARY KEY, metadata TEXT, gcs_path TEXT, original_filename TEXT, content_type TEXT, checksum TEXT)"""
        )
        self.conn.commit()
        logger.info("Database setup complete")

    def validate_consistency(self):
        c = self.conn.cursor()
        c.execute("SELECT count(1) FROM embeddings")
        entries = c.fetchone()[0]

        if not self.index.ntotal == entries:
            raise ValueError(
                f"DBs in inconsistent state: index count:{self.index.ntotal} vs metadata count: {entries}"
            )

    def _check_changed(self, blob, localfilename) -> bool:
        if not os.path.exists(localfilename):
            logger.debug(f"Local file {localfilename} does not exist")
            return True
        remote_md5 = blob.md5_hash
        if not remote_md5:
            logger.debug(f"No remote hash found for {localfilename}")
            raise ValueError("No remote hash found")
        md5 = hashlib.md5()
        with open(localfilename, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                md5.update(chunk)
        local_md5_digest = md5.digest()
        local_md5_base64 = base64.b64encode(local_md5_digest).decode("utf-8")
        logger.info(f"Local hash: {local_md5_base64} vs remote hash: {remote_md5}")
        return local_md5_base64 != remote_md5

    def load_index(self):
        logger.info(f"Loading index: {self.index_name}")
        index_blob = self.bucket.blob(f"{self.index_name}.index")

        if index_blob.exists():
            index_blob.reload()
            if self._check_changed(index_blob, f"{self.index_name}.index"):
                logger.info("Change detected. Downloading index from GCS")
                index_blob.download_to_filename(f"{self.index_name}.index")
                logger.info("Index downloaded from GCS")
            else:
                logger.info("Local index is up to date")
            self.index = faiss.read_index(f"{self.index_name}.index")
            logger.info("Index loaded")
        else:
            logger.info("No existing index found in GCS")

        db_blob = self.bucket.blob(self.db_name)
        if db_blob.exists():
            db_blob.reload()
            if self._check_changed(db_blob, self.db_name):
                logger.info("Change detected. Downloading database from GCS")
                db_blob.download_to_filename(self.db_name)
                logger.info("Database downloaded from GCS")
            else:
                logger.info("Local database is up to date")
        else:
            logger.info("No existing database found in GCS")

        if self.check_consistency:
            self.validate_consistency()

    def save_index(self):
        logger.info(f"Saving index: {self.index_name}")
        index_file_name = f"{self.index_name}.index"
        faiss.write_index(self.index, index_file_name)
        index_blob = self.bucket.blob(index_file_name)
        self.conn.commit()

        if self.check_consistency:
            logger.info("Checking consistency prior to save")
            self.validate_consistency()

        self.conn.close()
        index_blob.upload_from_filename(index_file_name, num_retries=3)
        logger.info("Index saved to GCS")

        db_blob = self.bucket.blob(self.db_name)
        db_blob.upload_from_filename(self.db_name, num_retries=3)
        logger.info("Database uploaded to GCS")

        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)

    def check_new(self, md5_hash):
        c = self.conn.cursor()
        result = c.execute(
            "SELECT EXISTS(SELECT 1 FROM embeddings WHERE checksum = ?);", (md5_hash,)
        ).fetchone()
        if result[0] == 1:
            logger.info("Preexisting entry, ignorning")
            return None
        return md5_hash

    def add_item(
        self, vector, metadata, raw_file_path, md5_hash, autosave=False
    ) -> int:
        logger.info(f"Adding item: {raw_file_path}")

        c = self.conn.cursor()
        c.execute("SELECT MAX(id) FROM embeddings")
        max_id = c.fetchone()[0]
        item_id = (max_id + 1) if max_id is not None else 0

        original_filename = os.path.basename(raw_file_path)
        content_type, _ = mimetypes.guess_type(raw_file_path)

        gcs_path = (
            f"{self.index_name}/{item_id}{os.path.splitext(original_filename)[1]}"
        )

        c.execute("SELECT id FROM embeddings WHERE checksum = ?", (md5_hash,))
        existing_id = c.fetchone()

        if existing_id:
            logger.info(
                f"Item with checksum {md5_hash} already exists in the database. Skipping addition."
            )
            return existing_id[0]

        self.index.add(np.array(vector).astype("float32"))
        logger.info(f"Vector added to index with ID: {item_id}")
        blob = self.bucket.blob(gcs_path)
        try:
            blob.upload_from_filename(
                raw_file_path, content_type=content_type, if_generation_match=0
            )
        except google.api_core.exceptions.PreconditionFailed:
            logger.info(
                f"File {gcs_path} already exists in the bucket. Skipping upload."
            )
        except google.auth.exceptions.TransportError as e:
            logger.error(
                f"TransportError occurred while uploading {gcs_path}: {str(e)}"
            )
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error occurred while uploading {gcs_path}: {str(e)}"
            )
            raise e

        c.execute(
            "INSERT INTO embeddings (id, metadata, gcs_path, original_filename, content_type, checksum) VALUES (?, ?, ?, ?, ?, ?)",
            (
                item_id,
                json.dumps(metadata),
                gcs_path,
                original_filename,
                content_type,
                md5_hash,
            ),
        )
        self.conn.commit()
        logger.info(f"Metadata added to database for item ID: {item_id}")

        if autosave:
            self.save_index()
            logger.info("Index autosaved")

        return item_id

    def search(self, query_vector, k=10):
        logger.info(f"Performing search with k={k}")
        query_vector = np.array([query_vector]).astype("float32")
        faiss.normalize_L2(query_vector)

        distances, indices = self.index.search(query_vector, k)
        logger.info(f"Search completed. Found {len(indices[0])} results.")

        results = []
        c = self.conn.cursor()
        for i, idx in enumerate(indices[0]):
            c.execute(
                "SELECT metadata, gcs_path, original_filename, content_type FROM embeddings WHERE id = ?",
                (int(idx),),
            )
            row = c.fetchone()
            if row:
                metadata, gcs_path, original_filename, content_type = row
                results.append(
                    {
                        "id": int(idx),
                        "distance": float(distances[0][i]),
                        "metadata": json.loads(metadata),
                        "gcs_path": self.bucket.blob(gcs_path),
                        "original_filename": original_filename,
                        "content_type": content_type,
                    }
                )
        logger.info(f"Retrieved metadata for {len(results)} results")
        return results
