#!/usr/bin/env bash
# Run only the REST API bundle on port 8000.
set -e
cd "$(dirname "$0")/.."
export DJANGO_BUNDLE=api
python manage.py runserver 8000
