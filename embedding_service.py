
from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):
        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Embedding model loaded successfully!")

    def generate_embedding(self, text):
        """
        Generate an embedding for a single text.
        """

        embedding = self.model.encode(text)

        return embedding.tolist()

    def generate_embeddings(self, texts):
        """
        Generate embeddings for multiple text chunks.
        """

        embeddings = self.model.encode(texts)

        return embeddings.tolist()


# Create one reusable embedding service
embedding_service = EmbeddingService()
