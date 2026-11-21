
from pdf_processor import (
    extract_text_from_pdf,
    split_text_into_chunks,
    process_pdf
)


def test_split_text_into_chunks():
    text = "Python is easy to learn. " * 200

    chunks = split_text_into_chunks(
        text,
        chunk_size=100,
        overlap=20
    )

    assert len(chunks) > 0
    assert all(len(chunk.split()) <= 100 for chunk in chunks)


def test_invalid_chunk_size():
    try:
        split_text_into_chunks("Python", chunk_size=0)
        assert False, "Expected ValueError"
    except ValueError:
        assert True


def test_process_pdf():
    chunks = process_pdf("sample.pdf")

    assert len(chunks) > 0
    assert "chunk_id" in chunks[0]
    assert "page_number" in chunks[0]
    assert "text" in chunks[0]


def test_extract_text_from_pdf():
    pages = extract_text_from_pdf("sample.pdf")

    assert len(pages) > 0
    assert "page_number" in pages[0]
    assert "text" in pages[0]
