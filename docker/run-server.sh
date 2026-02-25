#!/usr/bin/env bash
#
# Cookiecutter Django CMS with Docker support
# This cookiecutter provides a production ready Django CMS template using Docker.
#
# https://github.com/guma44/cookiecutter-django-cms-docker
#


# end when error
set -e
# raise error when variable is unset
set -u
# raise error when in pipe
set -o pipefail


if (( $# != 1 )); then
    echo "Ussage: run_server.sh [local|gunicorn]"
	exit
fi

if [ "$1" == "local" ]; then
	echo "Running local development server"
	echo "Python warnings are enabled"
	export WERKZEUG_DEBUG_PIN="off"
#	python3 $DJANGO_PROJECT_DIR/manage.py migrate
	python3 -W always $DJANGO_PROJECT_DIR/manage.py runserver_plus 0.0.0.0:8000  --noreload
elif [ "$1" == "gunicorn" ]; then
	echo "Running Gunicorn"
	python3 manage.py migrate
	python3 manage.py collectstatic --noinput
	gunicorn -c "python:config.gunicorn"
else
	echo "Usage: run_server.sh [local|gunicorn]"
fi
