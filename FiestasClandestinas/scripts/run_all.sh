#!/usr/bin/env bash
# Run the full monolith (all endpoints) on port 8000.
set -e
cd "$(dirname "$0")/.."
export DJANGO_BUNDLE=all
python manage.py runserver 8000
