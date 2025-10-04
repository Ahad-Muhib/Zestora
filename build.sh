#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files with force
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Check if static files were collected properly
echo "Checking static files..."
ls -la staticfiles/css/ | head -5

echo "Build completed successfully!"