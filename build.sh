#!/bin/bash

echo "🚀 Starting build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Apply database migrations
echo "🛠️ Applying migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Set permissions for execution (only needed once)
chmod +x build.sh

echo "✅ Build script completed successfully!"
