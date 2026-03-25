# Base image that includes `uv` for dependency management
FROM ghcr.io/astral/uv:latest as base

# Set working directory
WORKDIR /app

# Environment
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

# Copy dependency manifests first for efficient caching
COPY pyproject.toml uv.lock ./

# Install system build dependencies required for mysqlclient
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
  default-libmysqlclient-dev \
  build-essential \
  pkg-config \
  && rm -rf /var/lib/apt/lists/*

# Use `uv` to create and sync the isolated environment
RUN uv sync --yes

# Copy application code
COPY reservation_system/ ./reservation_system/

# Create a non-root user and fix permissions
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Run migrations inside the uv environment
RUN uv run python reservation_system/manage.py migrate --noinput

# Expose application port
EXPOSE 8000

# Healthcheck (uses uv run to ensure environment commands execute correctly)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD uv run python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/').read()" || exit 1

# Start the app via uv to ensure the uv-managed environment is used
CMD ["uv", "run", "uvicorn", "reservation_system.asgi:application", "--host", "0.0.0.0", "--port", "8000"]

