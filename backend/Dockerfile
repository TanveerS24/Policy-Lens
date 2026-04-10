FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update -o Acquire::Retries=5 -o Acquire::ForceIPv4=true && \
    apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir --default-timeout=1000 --retries 10 -r requirements.txt

COPY ./app ./app

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]