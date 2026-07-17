#!/usr/bin/env bash
# Run automated tests for the backend.
# Usage: ./test.sh
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"

echo "==> Running backend tests (Django)"
cd "$BACKEND_DIR"
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
python -m pip install -r requirements.txt
python manage.py test customers
