#!/usr/bin/env bash
# Apply migrations and load seed data.
set -e
cd "$(dirname "$0")/.."
python manage.py migrate
python manage.py loaddata seed.json
echo "Seed loaded OK."
