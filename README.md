# Demo App: Django + MySQL + Next.js (TypeScript)

This repository contains a simple **customer data management demo app** to help non-technical AI builders understand full-stack app structure.

- **Backend:** Django (MVT pattern)
- **Database:** MySQL (with SQLite fallback for local quick start)
- **Frontend:** Next.js with TypeScript
- **PII Security:** AES-256 encryption/decryption in backend for phone and address
- **Tests:** Django unit tests for encryption and API behavior

## 1) Project Structure

- `/backend` - Django app (`customers`) using MVT
- `/frontend` - Next.js TypeScript UI

## 2) Backend Setup (Django)

```bash
cd /home/runner/work/demo-app-python/demo-app-python/backend
python -m pip install -r requirements.txt
```

### Configure environment variables

```bash
export DJANGO_DEBUG=true
export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Optional MySQL settings (if set, Django uses MySQL)
export MYSQL_DATABASE=demo_app
export MYSQL_USER=root
export MYSQL_PASSWORD=root
export MYSQL_HOST=localhost
export MYSQL_PORT=3306

# AES-256 encryption key for PII (recommended in real deployments)
export PII_ENCRYPTION_KEY="replace-with-strong-secret"
```

> If `MYSQL_DATABASE` is not set, Django uses SQLite for quick local development.

### Run backend

```bash
python manage.py migrate
python manage.py runserver
```

Django MVT page: `http://localhost:8000/`

API endpoint for frontend: `http://localhost:8000/api/customers/`

## 3) Frontend Setup (Next.js TypeScript)

```bash
cd /home/runner/work/demo-app-python/demo-app-python/frontend
npm install
```

Set API URL (optional, default already points to localhost backend):

```bash
export NEXT_PUBLIC_API_BASE_URL="http://localhost:8000/api/customers/"
```

Run frontend:

```bash
npm run dev
```

Open: `http://localhost:3000/`

## 4) AES-256 PII Encryption Notes

In the Django `Customer` model:
- `phone_encrypted` and `address_encrypted` are what gets stored in DB.
- `phone` and `address` properties decrypt values for display.
- Encryption uses AES-GCM with a 256-bit key.

## 5) Unit Tests

Run backend unit tests:

```bash
cd /home/runner/work/demo-app-python/demo-app-python/backend
python manage.py test customers
```

Included tests validate:
- encryption/decryption round-trip
- encrypted storage (no plaintext PII in DB fields)
- customer API create/list behavior
