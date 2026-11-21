
from uuid import uuid4

from embedding_service import embedding_service
from vector_store import vector_store


def test_store_and_search_chunks():
    document_id = str(uuid4())
    user_id = 1

    chunks = [
        {
            "chunk_id": 1,
            "page_number": 1,
            "text": "Python is a programming language."
        }
    ]

    embeddings = embedding_service.generate_embeddings(
        [chunks[0]["text"]]
    )

    vector_store.store_chunks(
        chunks,
        embeddings,
        document_id,
        user_id=user_id
    )

    query_embedding = embedding_service.generate_embeddings(
        ["What is Python?"]
    )[0]

    results = vector_store.search_similar_chunks(
        query_embedding=query_embedding,
        user_id=user_id,
        limit=3
    )

    assert len(results) > 0
    assert any(
        result.payload["document_id"] == document_id
        for result in results
    )
