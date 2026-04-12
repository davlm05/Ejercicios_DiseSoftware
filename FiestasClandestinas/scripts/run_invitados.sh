#!/usr/bin/env bash
# Run only the invitados SSR frontend on port 8001.
set -e
cd "$(dirname "$0")/.."
export DJANGO_BUNDLE=invitados
python manage.py runserver 8001
