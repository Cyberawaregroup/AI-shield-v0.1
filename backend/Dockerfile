ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_CACHE_DIR=/tmp/uv-cache

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    gnupg \
    ca-certificates \
    git \
    build-essential \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
# Set the working directory
WORKDIR /app

# Copy project configuration files
COPY pyproject.toml uv.lock ./

# Synchronize dependencies
RUN uv sync --no-cache-dir

ENV DISPLAY=:99

# Copy the rest of the application code
COPY . .

# Create necessary directories
RUN mkdir -p logs uploads

# Expose the default port for the web application
EXPOSE 8000

ENV ENVIRONMENT=staging

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
