#!/usr/bin/env bash
# One-shot setup + run for the Django backend and Vite frontend.
# Usage: ./run.sh
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

echo "==> Setting up backend (Django)"
cd "$BACKEND_DIR"
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate

echo "==> Setting up frontend (Vite)"
cd "$FRONTEND_DIR"
npm install

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
  echo ""
  echo "==> Shutting down servers"
  [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null
  [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null
}
trap cleanup EXIT INT TERM

echo "==> Starting backend on http://localhost:8000"
cd "$BACKEND_DIR"
source venv/bin/activate
python manage.py runserver &
BACKEND_PID=$!

echo "==> Starting frontend on http://localhost:5173"
cd "$FRONTEND_DIR"
npm run dev &
FRONTEND_PID=$!

wait "$BACKEND_PID" "$FRONTEND_PID"
