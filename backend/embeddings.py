import threading
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingModel:
	_instance = None
	_lock = threading.Lock()

	def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
		self.model_name = model_name
		self.model = SentenceTransformer(model_name)

	@classmethod
	def get_instance(cls) -> "EmbeddingModel":
		if cls._instance is None:
			with cls._lock:
				if cls._instance is None:
					cls._instance = EmbeddingModel()
		return cls._instance

	def embed_texts(self, texts: List[str]) -> np.ndarray:
		embeddings = self.model.encode(texts, normalize_embeddings=True, convert_to_numpy=True, batch_size=64, show_progress_bar=False)
		return embeddings.astype(np.float32)

	def embed_text(self, text: str) -> np.ndarray:
		return self.embed_texts([text])[0]

