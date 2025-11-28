@echo off

echo Activating virtual environment...
call venv\Scripts\activate

echo Waiting for database...
python manage.py wait_for_db

echo Starting Django server...
python manage.py runserver

pause

