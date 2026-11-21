
import os
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)


class VectorStore:

    def __init__(self):

        self.client = QdrantClient(
            url=os.getenv(
                "QDRANT_URL",
                "http://localhost:6333"
            )
        )

        self.collection_name = "teacher_documents"

        self.create_collection()

    def create_collection(self):

        if not self.client.collection_exists(
            self.collection_name
        ):

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

            print("PDF collection created successfully!")

        else:

            print("PDF collection already exists!")

    def store_chunks(
        self,
        chunks,
        embeddings,
        document_id,
        user_id
    ):

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match."
            )

        points = []

        for chunk, embedding in zip(chunks, embeddings):

            point = PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "document_id": document_id,
                    "user_id": user_id,
                    "chunk_id": chunk["chunk_id"],
                    "page_number": chunk["page_number"],
                    "text": chunk["text"]
                }
            )

            points.append(point)

        if points:

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

        print(f"{len(points)} chunks stored successfully!")

    def search_similar_chunks(
        self,
        query_embedding,
        user_id,
        limit=3
    ):

        user_filter = Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id)
                )
            ]
        )

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            query_filter=user_filter,
            limit=limit,
            with_payload=True
        ).points

        return results


# Create reusable vector store
vector_store = VectorStore()
