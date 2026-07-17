@echo off
REM Run automated tests for the backend.
REM Usage: test.bat

set ROOT_DIR=%~dp0
set BACKEND_DIR=%ROOT_DIR%backend

echo ==> Running backend tests (Django)
cd /d "%BACKEND_DIR%"
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install -r requirements.txt
if errorlevel 1 goto :error
python manage.py test customers
if errorlevel 1 goto :error
goto :eof

:error
echo Tests failed. See errors above.
exit /b 1
