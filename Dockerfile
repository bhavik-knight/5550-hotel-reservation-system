FROM python:3.13-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy dependency files first for caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy the rest of the application
COPY . .

FROM python:3.13-slim AS runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv in the runtime stage as well
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy the virtual environment and the application from the builder
COPY --from=builder /app /app

# Port configuration
EXPOSE 8000

# Set the working directory to where manage.py is
WORKDIR /app/reservation_system

# Default command matches local uvicorn usage
CMD ["sh", "-c", "uv run python manage.py migrate && uv run python manage.py seed_data && uv run uvicorn reservation_system.asgi:application --host 0.0.0.0 --port 8000"]