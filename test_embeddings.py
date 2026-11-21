
from embedding_service import embedding_service


def test_generate_embeddings():
    texts = [
        "Python is a programming language.",
        "FastAPI is a Python web framework."
    ]

    embeddings = embedding_service.generate_embeddings(texts)

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384
    assert len(embeddings[1]) == 384


def test_embedding_values_are_valid():
    texts = ["This is a test sentence."]

    embeddings = embedding_service.generate_embeddings(texts)

    assert len(embeddings) == 1
    assert all(
        isinstance(value, float)
        for value in embeddings[0]
    )
