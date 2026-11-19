
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from uuid import uuid4

# Connect to Qdrant
client = QdrantClient(url="http://localhost:6333")

# Load the embedding model
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Collection name
collection_name = "teacher_documents"

# Sample documents
documents = [
    "Python is a popular programming language.",
    "Java is widely used for software development.",
    "Machine learning helps computers learn from data.",
    "Artificial intelligence makes machines intelligent.",
    "PostgreSQL is a relational database management system.",
    "FastAPI is a Python framework for building APIs."
]

# Generate embeddings
print("\nGenerating embeddings...")
embeddings = model.encode(documents)

# Prepare data for Qdrant
points = []

for document, embedding in zip(documents, embeddings):
    point = PointStruct(
        id=str(uuid4()),
        vector=embedding.tolist(),
        payload={
            "text": document
        }
    )

    points.append(point)

# Store documents and embeddings
client.upsert(
    collection_name=collection_name,
    points=points
)

print("\nDocuments stored successfully in Qdrant!")

# Verify stored documents
result = client.scroll(
    collection_name=collection_name,
    limit=10,
    with_payload=True,
    with_vectors=False
)

print("\nStored documents:")

for point in result[0]:
    print("-", point.payload["text"])

print("\nTotal documents inserted:", len(points))
