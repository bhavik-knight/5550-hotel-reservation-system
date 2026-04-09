#!/bin/bash
set -e

echo "🏨 Hotel Reservation System - Local Setup"
echo "=========================================="

# 1. Ensure .env exists (copy from example if not)
if [ ! -f .env ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
fi

# 2. Sync dependencies
echo "📦 Syncing dependencies with uv..."
uv sync

# 3. Run migrations
echo "🗄️  Running migrations..."
uv run python reservation_system/manage.py migrate

# 4. Seed data
echo "🌱 Seeding realistic mock data (20 Hotels, 250 Reservations)..."
uv run python reservation_system/manage.py seed_data --hotels 20 --reservations 250

echo ""
echo "✅ Local setup complete!"
echo ""
echo "🚀 To start the server, run:"
echo "   uv run uvicorn --app-dir reservation_system reservation_system.asgi:application --reload"
echo ""
echo "📊 Accessible at: http://localhost:8000/api/docs/"
