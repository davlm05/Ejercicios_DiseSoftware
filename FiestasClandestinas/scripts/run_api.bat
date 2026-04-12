@echo off
REM Run only the REST API bundle on port 8000.
cd /d "%~dp0.."
set DJANGO_BUNDLE=api
python manage.py runserver 8000
