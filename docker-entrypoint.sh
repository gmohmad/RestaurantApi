#!/bin/bash
set -e

case "$1" in
web)
  alembic upgrade a92e977974a8
  uvicorn src.main:app --host 0.0.0.0
  ;;
test)
  pytest -v tests/
  ;;
*)
  exec "$@"
  ;;
esac
