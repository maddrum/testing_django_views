#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -e

pwd
pip install -r requirements.txt --user

if [ -f "manage.py" ]; then
  python manage.py migrate --noinput
fi

exec "$@"
