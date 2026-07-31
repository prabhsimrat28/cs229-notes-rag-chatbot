FROM python:3.11-slim

WORKDIR /app

# System deps needed to build some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install backend-only dependencies first (better layer caching)
COPY requirements-backend.txt .
RUN pip install --no-cache-dir -r requirements-backend.txt

# Copy the rest of the project (frontend.py, data/, etc. are excluded via .dockerignore)
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
