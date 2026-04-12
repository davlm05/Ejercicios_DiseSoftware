@echo off
REM Run only the localizacion SSR frontend on port 8002.
cd /d "%~dp0.."
set DJANGO_BUNDLE=localizacion
python manage.py runserver 8002
