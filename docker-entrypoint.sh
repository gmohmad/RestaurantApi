#!/bin/bash
set -e

case "$1" in
web)
  alembic upgrade head
  uvicorn src.main:app --host 0.0.0.0
  ;;
test)
  pytest -v tests/
  ;;
*)
  exec "$@"
  ;;
esac
