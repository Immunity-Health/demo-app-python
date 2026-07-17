@echo off
REM One-shot setup + run for the Django backend and Vite frontend.
REM Usage: run.bat

set ROOT_DIR=%~dp0
set BACKEND_DIR=%ROOT_DIR%backend
set FRONTEND_DIR=%ROOT_DIR%frontend

echo ==> Setting up backend (Django)
cd /d "%BACKEND_DIR%"
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python manage.py migrate
if errorlevel 1 goto :error

echo ==> Setting up frontend (Vite)
cd /d "%FRONTEND_DIR%"
call npm install
if errorlevel 1 goto :error

echo ==> Starting backend on http://localhost:8000
start "Backend (Django)" cmd /k "cd /d "%BACKEND_DIR%" && call venv\Scripts\activate.bat && python manage.py runserver"

echo ==> Starting frontend on http://localhost:5173
start "Frontend (Vite)" cmd /k "cd /d "%FRONTEND_DIR%" && npm run dev"

echo ==> Both servers are starting in separate windows. Close those windows to stop them.
goto :eof

:error
echo Setup failed. See errors above.
exit /b 1
