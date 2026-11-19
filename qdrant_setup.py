
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Connect to Qdrant
client = QdrantClient(url="http://localhost:6333")

# Collection name
collection_name = "teacher_documents"

# Check whether collection already exists
if client.collection_exists(collection_name):
    print("Collection already exists!")
else:
    # Create collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    print("Collection created successfully!")

# Display collections
collections = client.get_collections()

print("\nAvailable collections:")
for collection in collections.collections:
    print(collection.name)
