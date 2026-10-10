# ==============================================================================
# Google Cloud Build Production Dockerfile
# Base Image: Python 3.11-slim (Optimized Debian Bullseye/Bookworm minimal runtime)
# Target Service: Google Cloud Run Serverless Container
# ==============================================================================

FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install security updates and curl for container health check
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies in separate layer for optimal caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create a non-root system user with explicit UID for GCP container security compliance
RUN useradd -u 1000 -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Container Healthcheck for Google Cloud Run / Container Orchestration
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/health || exit 1

# Expose target HTTP port
EXPOSE 8080

# Production Gunicorn WSGI server entrypoint
CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 main:app
