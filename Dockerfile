
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# Install CPU-only PyTorch
RUN python -m pip install --no-cache-dir \
    --default-timeout=120 \
    --retries=10 \
    --index-url https://download.pytorch.org/whl/cpu \
    --extra-index-url https://pypi.org/simple \
    torch

# Install remaining project dependencies
RUN python -m pip install --no-cache-dir \
    --default-timeout=120 \
    --retries=10 \
    -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
