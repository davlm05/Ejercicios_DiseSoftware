@echo off
REM Run the full monolith (all endpoints) on port 8000.
cd /d "%~dp0.."
set DJANGO_BUNDLE=all
python manage.py runserver 8000
