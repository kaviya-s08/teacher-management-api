
import os
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

from auth import get_current_user
from models import User

from schemas import (
    SemanticSearchRequest,
    SemanticSearchResponse,
    SemanticSearchResult
)


# Create API router
router = APIRouter(
    prefix="/semantic-search",
    tags=["Semantic Search"]
)


# Qdrant configuration
QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://localhost:6333"
)

COLLECTION_NAME = "teacher_documents"


# Connect to Qdrant
client = QdrantClient(url=QDRANT_URL)


# Load model only when needed
@lru_cache(maxsize=1)
def get_embedding_model():

    print("Loading semantic search embedding model...")

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Semantic search model loaded successfully!")

    return model


@router.post(
    "",
    response_model=SemanticSearchResponse
)
def search_documents(
    request: SemanticSearchRequest,
    current_user: User = Depends(get_current_user)
):

    try:
        # Get embedding model
        model = get_embedding_model()

        # Convert query into embedding
        query_embedding = model.encode(
            request.query
        ).tolist()

        # Search Qdrant
        search_results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=request.limit,
            with_payload=True
        ).points

        # Prepare response
        results = []

        for point in search_results:

            if point.payload and "text" in point.payload:

                results.append(
                    SemanticSearchResult(
                        text=point.payload["text"],
                        score=round(float(point.score), 4)
                    )
                )

        return SemanticSearchResponse(
            query=request.query,
            results=results
        )

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Semantic search service is temporarily unavailable."
        )
