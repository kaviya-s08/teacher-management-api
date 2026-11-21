
import os
import tempfile
from uuid import uuid4

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from pydantic import BaseModel, Field

from auth import get_current_user
from models import User

from pdf_processor import process_pdf
from embedding_service import embedding_service
from vector_store import vector_store
from ai import get_ai_response


router = APIRouter(
    prefix="/rag",
    tags=["RAG PDF Question Answering"]
)


# Request model for asking questions
class AskRequest(BaseModel):

    question: str = Field(
        min_length=1,
        max_length=2000
    )

    top_k: int = Field(
        default=3,
        ge=1,
        le=10
    )


# --------------------------------------------------
# PDF UPLOAD ENDPOINT
# --------------------------------------------------

@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF content type."
        )

    document_id = str(uuid4())
    temp_path = None

    try:

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty."
            )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(contents)
            temp_path = temp_file.name

        chunks = process_pdf(temp_path)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No extractable text found in PDF."
            )

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = embedding_service.generate_embeddings(
            texts
        )

        vector_store.store_chunks(
            chunks,
            embeddings,
            document_id,
            current_user.id
        )

        return {
            "message": "PDF uploaded and processed successfully.",
            "document_id": document_id,
            "filename": file.filename,
            "total_chunks": len(chunks),
            "status": "success"
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="PDF processing failed."
        )

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        await file.close()


# --------------------------------------------------
# RAG QUESTION ANSWERING ENDPOINT
# --------------------------------------------------

@router.post("/ask")
async def ask_question(
    request: AskRequest,
    current_user: User = Depends(get_current_user)
):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty."
        )

    try:

        # Step 1: Generate question embedding
        query_embedding = embedding_service.generate_embedding(
            question
        )

        # Step 2: Search the user's PDF chunks
        results = vector_store.search_similar_chunks(
            query_embedding=query_embedding,
            user_id=current_user.id,
            limit=request.top_k
        )

        if not results:

            raise HTTPException(
                status_code=404,
                detail="No uploaded PDF content found. Upload a PDF first."
            )

        # Step 3: Prepare retrieved context
        context_parts = []

        sources = []

        for result in results:

            payload = result.payload or {}

            text = payload.get("text", "")

            if not text:
                continue

            page_number = payload.get(
                "page_number"
            )

            context_parts.append(
                f"Page {page_number}:\n{text}"
            )

            sources.append({
                "document_id": payload.get("document_id"),
                "page_number": page_number,
                "score": result.score
            })

        if not context_parts:

            raise HTTPException(
                status_code=404,
                detail="No relevant PDF text was found."
            )

        context = "\n\n".join(context_parts)

        # Step 4: Generate answer using Groq
        system_prompt = (
            "You are a PDF question-answering assistant. "
            "Answer the user's question using only the supplied PDF context. "
            "Do not invent facts or use outside knowledge. "
            "If the answer is not present in the context, "
            "clearly say that the information was not found in the uploaded PDF. "
            "Mention page numbers when useful."
        )

        user_prompt = (
            f"PDF CONTEXT:\n{context}\n\n"
            f"USER QUESTION:\n{question}\n\n"
            "Answer based only on the PDF context."
        )

        answer = await get_ai_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        # Step 5: Return answer and sources
        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "status": "success"
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="RAG question answering failed."
        )
