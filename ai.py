
import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from groq import (
    AsyncGroq,
    APITimeoutError,
    APIConnectionError,
    AuthenticationError,
    RateLimitError,
    APIStatusError,
    APIError,
)

# Load environment variables
load_dotenv()

# Create AI router
router = APIRouter(prefix="/ai", tags=["AI"])

# Model configuration
MODEL_NAME = "openai/gpt-oss-20b"


# Request schema for generating responses
class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=8000)


# Request schema for summarization
class SummarizeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20000)


# Common function to communicate with Groq
async def get_ai_response(system_prompt: str, user_prompt: str):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="Groq API key is not configured."
        )

    try:
        async with AsyncGroq(
            api_key=api_key,
            timeout=30.0,
            max_retries=1
        ) as client:

            completion = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                max_completion_tokens=1024,
                temperature=0.5
            )

            response = completion.choices[0].message.content

            if not response:
                raise HTTPException(
                    status_code=502,
                    detail="AI returned an empty response."
                )

            return response.strip()

    except APITimeoutError:
        raise HTTPException(
            status_code=504,
            detail="AI request timed out. Please try again."
        )

    except APIConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to AI service."
        )

    except AuthenticationError:
        raise HTTPException(
            status_code=502,
            detail="AI service authentication failed. Check API configuration."
        )

    except RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="AI API rate limit exceeded. Please try again later."
        )

    except APIStatusError as error:
        raise HTTPException(
            status_code=502,
            detail=f"AI service returned an error (status {error.status_code})."
        )

    except APIError:
        raise HTTPException(
            status_code=502,
            detail="An AI service error occurred."
        )


# POST /ai/generate
@router.post("/generate")
async def generate_response(request: GenerateRequest):

    if not request.prompt.strip():
        raise HTTPException(
            status_code=422,
            detail="Prompt cannot be empty."
        )

    response = await get_ai_response(
        system_prompt="You are a helpful AI assistant. Give clear and accurate answers.",
        user_prompt=request.prompt
    )

    return {
        "response": response
    }


# POST /ai/summarize
@router.post("/summarize")
async def summarize_text(request: SummarizeRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=422,
            detail="Text cannot be empty."
        )

    response = await get_ai_response(
        system_prompt=(
            "You are a professional summarization assistant. "
            "Summarize the given text clearly and concisely. "
            "Preserve the important information."
        ),
        user_prompt=request.text
    )

    return {
        "summary": response
    }
