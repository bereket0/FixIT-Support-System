#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist (optional)
echo "Build completed successfully!" 