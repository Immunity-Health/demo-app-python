# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A demo customer data management app pairing a Django backend (MVT pattern, app `customers`) with a React + TypeScript (Vite) frontend, built to help non-technical AI builders understand full-stack structure. Database is MySQL with a SQLite fallback for local dev. Notable feature: AES-256-GCM encryption of PII fields (phone, address, Aadhar number) at rest.

## Commands

### Setup + run everything
```bash
./run.sh          # macOS/Linux: sets up venv + npm deps, runs migrations, starts both dev servers
run.bat           # Windows equivalent
```
- Django serves at `http://localhost:8000/`, React at `http://localhost:5173/` (Vite proxies `/api` to Django — see `frontend/vite.config.ts`).

### Backend (from `backend/`)
```bash
python -m venv venv && source venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend (from `frontend/`)
```bash
npm install
npm run dev       # dev server
npm run build     # tsc -b type-check + vite build
npm run lint      # eslint
npm run preview
```

### Tests
```bash
./test.sh         # macOS/Linux: sets up venv/deps if needed, runs Django test suite
test.bat          # Windows equivalent
```
Equivalent to `cd backend && python manage.py test customers`. Run a single test with e.g. `python manage.py test customers.tests.CustomerTests.test_customer_api_create_and_list`.

There is no frontend test suite currently.

## Architecture

### Backend (`backend/`)
- Single Django app `customers` handles everything; `config/` holds project settings/urls/wsgi/asgi.
- `customers/models.py` — `Customer` model stores PII in `*_encrypted` TextFields (`phone_encrypted`, `address_encrypted`, `aadhar_number_encrypted`). Plaintext is never persisted directly: Python properties (`phone`, `address`, `aadhar_number`) transparently encrypt on set and decrypt on get, so callers just do `customer.phone = "..."` / read `customer.phone` like normal fields.
- `customers/encryption.py` — AES-256-GCM via `cryptography.hazmat`. `PII_ENCRYPTION_KEY` env var is the key; if given as urlsafe-base64 of exactly 32 bytes it's used directly, otherwise it's SHA-256-hashed into a key. `config/settings.py` falls back to a key derived from `SECRET_KEY` if `PII_ENCRYPTION_KEY` is unset — fine for the demo, but any change to key derivation invalidates previously-encrypted DB values.
- `customers/forms.py` — `CustomerForm` is a `ModelForm` with extra plain `CharField`s (`phone`, `address`, `aadhar_number`) that mirror the encrypted properties; `save()` explicitly routes cleaned data through the model properties (not model fields) so encryption happens on write.
- `customers/views.py` — two parallel surfaces for the same data:
  - Server-rendered views (`customer_list`, `customer_delete`) backing Django templates in `customers/templates/`.
  - A small JSON API (`customer_api`, both GET/POST at `/api/customers/`) consumed by the React frontend. It's `@csrf_exempt` and hand-rolls request parsing (no DRF) — any change here must keep both request shapes working.
- DB selection in `config/settings.py`: set `MYSQL_DATABASE` (+ `MYSQL_USER`/`PASSWORD`/`HOST`/`PORT`) to use MySQL; otherwise it falls back to local `db.sqlite3`.

### Frontend (`frontend/`)
- Vite + React 19 + TypeScript, routed with `react-router-dom`. `App.tsx` is the shell (header/nav) rendering an `<Outlet />`; page components live in `src/pages` (currently `CustomersPage.tsx`), shared types in `src/types`.
- Talks to the backend only through `/api/customers/`, which Vite's dev server proxies to `http://127.0.0.1:8000` (see `frontend/vite.config.ts`) — the Django server must be running for the frontend to have data locally.
- Uses the React Compiler Babel plugin (`@rolldown/plugin-babel` + `babel-plugin-react-compiler`) wired in `vite.config.ts`; keep this in mind if adding/upgrading Babel or Vite plugins since it's a less common setup than plain `@vitejs/plugin-react`.

## Working with PII fields

When adding a new sensitive field, follow the existing pattern end-to-end rather than adding a plain model field: encrypted `TextField` on the model + property getter/setter through `encryption.py`, plumbed through `CustomerForm`, and exposed in the `customer_api` JSON shape in `views.py`. Missing any one of these layers will silently store or leak plaintext.
