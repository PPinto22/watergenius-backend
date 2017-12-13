#!/bin/sh
# set -e

mkdir -p log data

cd watergenius_api

ls -lsa

python3.6 manage.py collectstatic --noinput
python3.6 manage.py migrate --noinput

exec "$@"