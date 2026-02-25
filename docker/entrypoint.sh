#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -e

pip3 install -r requirements.txt
python manage.py migrate --noinput

exec "$@"
