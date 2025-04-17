import faiss
import pickle
import numpy as np

class FAISSIndex:
    def __init__(self, vector_size=768):
        self.index = faiss.IndexFlatL2(vector_size)
        self.metadata = []

    def add_data(self, embeddings, metadata):
        self.index.add(np.array(embeddings).astype('float32'))
        self.metadata.extend(metadata)

    def search(self, query_embedding, k=3):
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)
        results = [self.metadata[i] for i in indices[0] if i < len(self.metadata)]
        return results

    def save_index(self, filename="app/faiss/vector_store.pkl"):
        with open(filename, "wb") as f:
            pickle.dump((self.index, self.metadata), f)

    def load_index(self, filename="app/faiss/vector_store.pkl"):
        with open(filename, "rb") as f:
            self.index, self.metadata = pickle.load(f)
