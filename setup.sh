#!/bin/bash

# Hotel Reservation System - Secure Setup Script
# This script helps you set up the environment securely

set -e

echo "🏨 Hotel Reservation System - Secure Setup"
echo "=========================================="
echo ""

# Check if .env already exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
fi

# Create .env file
echo "📝 Creating .env file..."
cp .env.example .env

# Generate Django SECRET_KEY
echo "🔐 Generating Django SECRET_KEY..."
SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
sed -i.bak "s|SECRET_KEY=|SECRET_KEY=$SECRET_KEY|" .env && rm .env.bak

# Prompt for database passwords
echo ""
echo "Please enter your database passwords:"
echo "(passwords will not be displayed)"
echo ""

read -sp "MySQL Root Password: " MYSQL_ROOT_PASSWORD
echo ""
read -sp "Database User Password: " DB_PASSWORD
echo ""

# Update .env file
sed -i.bak "s|DB_PASSWORD=|DB_PASSWORD=$DB_PASSWORD|" .env && rm .env.bak
sed -i.bak "s|MYSQL_ROOT_PASSWORD=|MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD|" .env && rm .env.bak

echo ""
echo "✅ Environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Review your .env file"
echo "2. Run: docker compose up --build -d"
echo "3. Access the API at: http://localhost:8000"
echo ""
echo "⚠️  IMPORTANT: Never commit .env to version control!"
