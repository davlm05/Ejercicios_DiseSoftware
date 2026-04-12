#!/usr/bin/env bash
# Run only the localización SSR frontend on port 8002.
set -e
cd "$(dirname "$0")/.."
export DJANGO_BUNDLE=localizacion
python manage.py runserver 8002
