@echo off
REM Run only the invitados SSR frontend on port 8001.
cd /d "%~dp0.."
set DJANGO_BUNDLE=invitados
python manage.py runserver 8001
