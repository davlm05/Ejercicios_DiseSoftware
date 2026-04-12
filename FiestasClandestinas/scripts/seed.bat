@echo off
REM Apply migrations and load seed data.
cd /d "%~dp0.."
python manage.py migrate
python manage.py loaddata seed.json
echo Seed loaded OK.
