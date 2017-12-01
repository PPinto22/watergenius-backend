#!/bin/sh
# set -e

mkdir -p log data

cd watergenius_api

ls -lsa

#python3.4 manage.py collectstatic --noinput
#python3.4 manage.py migrate --noinput

exec "$@"