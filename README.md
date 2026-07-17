# Demo App: Django + MySQL + React (Vite + TypeScript)

A simple **customer data management demo app** to help non-technical AI builders understand full-stack app structure.

- **Backend:** Django (MVT pattern)
- **Database:** MySQL (with SQLite fallback for local quick start)
- **Frontend:** React + TypeScript, built with Vite, routed with React Router
- **PII Security:** AES-256 encryption/decryption in backend for phone and address
- **Tests:** Django unit tests for encryption and API behavior

## Project Structure

- `/backend` - Django app (`customers`) using MVT
- `/frontend` - Vite + React + TypeScript SPA (`src/pages`, `src/types`, routed via `react-router-dom`)
- `run.sh` / `run.bat` - one-shot setup + run script for both servers
- `test.sh` / `test.bat` - one-shot setup + run script for automated tests

## Quick Start

Sets up the venv, installs backend/frontend dependencies, runs migrations, and starts both dev servers:

```bash
./run.sh          # macOS / Linux
```

```bat
run.bat           # Windows
```

- `run.sh` runs both servers in the background of the same terminal; `Ctrl+C` stops both.
- `run.bat` opens each server in its own console window; close a window to stop that server.

Once running:
- Django: `http://localhost:8000/`
- React app: `http://localhost:5173/` (proxies `/api` requests to Django — see `frontend/vite.config.ts`)

## Manual Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Optional environment variables (defaults use SQLite and a dev encryption key):

```bash
export DJANGO_DEBUG=true
export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Optional step: If set, Django uses MySQL instead of SQLite
export MYSQL_DATABASE=demo_app
export MYSQL_USER=root
export MYSQL_PASSWORD=root
export MYSQL_HOST=localhost
export MYSQL_PORT=3306

# AES-256 encryption key for PII (recommended in real deployments)
export PII_ENCRYPTION_KEY="replace-with-strong-secret"
```

### Frontend

```bash
cd frontend
npm install
npm run dev      # http://localhost:5173/
```

Other scripts: `npm run build` (type-check + production build), `npm run preview`, `npm run lint`.

## AES-256 PII Encryption Notes

In the Django `Customer` model:
- `phone_encrypted` and `address_encrypted` are what gets stored in DB.
- `phone` and `address` properties decrypt values for display.
- Encryption uses AES-GCM with a 256-bit key.

## Unit Tests

```bash
./test.sh         # macOS / Linux
test.bat          # Windows
```

Sets up the venv and dependencies if needed, then runs the Django `customers` test suite. Included tests validate:
- encryption/decryption round-trip
- encrypted storage (no plaintext PII in DB fields)
- customer API create/list behavior
