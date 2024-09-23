import torch
from PIL import Image
from transformers import AutoProcessor, SiglipModel
import numpy as np
from indexing import BaseIndexer
import faiss
import hashlib


class ImageSearch(BaseIndexer):
    def __init__(
        self,
        index_name,
        gcs_project,
        bucket_name,
        model_name="nielsr/siglip-base-patch16-224",
        vector_size=768,
        check_consistency=False,
    ):
        super().__init__(index_name, gcs_project, bucket_name, vector_size)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = SiglipModel.from_pretrained(model_name).to(self.device)
        self.check_consistency = check_consistency

    def extract_features(self, image):
        with torch.no_grad():
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            image_features = self.model.get_image_features(**inputs)
        return image_features.squeeze().cpu().numpy()

    def add_image(self, image_path, metadata):
        with open(image_path, "rb") as file:
            md5_hash = hashlib.md5(file.read()).hexdigest()
        assert md5_hash

        if not self.check_new(image_path):
            return None

        image = Image.open(image_path).convert("RGB")
        features = self.extract_features(image)
        vector = np.array([features]).astype("float32")
        faiss.normalize_L2(vector)
        item_id = self.add_item(vector, metadata, image_path, md5_hash)
        return item_id

    def search(self, input_image, num_results=9):
        input_features = self.extract_features(input_image)
        results = super().search(input_features, num_results)

        return results
