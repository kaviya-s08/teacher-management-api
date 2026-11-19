
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# Connect to Qdrant
client = QdrantClient(url="http://localhost:6333")

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Collection name
collection_name = "teacher_documents"

# Search query
query = "I want to learn about artificial intelligence"

# Convert query into embedding
query_embedding = model.encode(query).tolist()

# Search similar documents in Qdrant
search_results = client.query_points(
    collection_name=collection_name,
    query=query_embedding,
    limit=3,
    with_payload=True
).points

# Display results
print("\nSearch Query:", query)
print("\nMost similar documents:\n")

for result in search_results:
    print("Document:", result.payload["text"])
    print("Similarity Score:", round(result.score, 4))
    print("--------------------------------")

print("\nSemantic search completed!")
