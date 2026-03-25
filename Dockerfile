# Multi-stage build for optimized production image
FROM python:3.14-slim as base

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# Build stage - Install dependencies with uv
# ============================================
FROM base as builder

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy project files
COPY pyproject.toml uv.lock ./

# Create virtual environment with uv
RUN ~/.cargo/bin/uv venv --python 3.14 && \
    ~/.cargo/bin/uv pip install -r <(~/.cargo/bin/uv pip compile pyproject.toml --output-file -)

# ============================================
# Runtime stage - Minimal production image
# ============================================
FROM base as runtime

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Set PATH to use virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy project code
COPY reservation_system/ ./reservation_system/

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Run migrations
RUN cd reservation_system && \
    python manage.py migrate --noinput

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/ || exit 1

# Start Uvicorn server
CMD ["uvicorn", "reservation_system.asgi:application", "--host", "0.0.0.0", "--port", "8000"]

