
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    Extract text from every page of a PDF.
    """

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if text.strip():
            pages.append({
                "page_number": page_number,
                "text": text
            })

    return pages


def split_text_into_chunks(text, chunk_size=500, overlap=100):
    """
    Divide text into smaller chunks with overlap.
    """

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be between 0 and chunk_size.")

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def process_pdf(pdf_path):
    """
    Extract PDF text and create chunks with page information.
    """

    pages = extract_text_from_pdf(pdf_path)

    all_chunks = []

    chunk_id = 1

    for page in pages:

        chunks = split_text_into_chunks(
            page["text"],
            chunk_size=500,
            overlap=100
        )

        for chunk in chunks:

            all_chunks.append({
                "chunk_id": chunk_id,
                "page_number": page["page_number"],
                "text": chunk
            })

            chunk_id += 1

    return all_chunks
