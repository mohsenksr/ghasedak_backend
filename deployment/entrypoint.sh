#!/bin/bash

set -e


# There are some times database is not ready yet!
# We'll check if database is ready and we can connect to it
# then the rest of the code run as well.

echo "Waiting for database..."
echo DB_NAME: ${DB_NAME}
echo DB_HOST: ${DB_HOST}
echo DB_PORT: ${DB_PORT}
while ! nc -z ${DB_HOST} ${DB_PORT}; do sleep 1; done
echo "Connected to database."


# database migrations will migrate as soon as database is ready
# as a result the database structure is always matched with the recent changes!

python manage.py migrate --no-input
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to migrate database: $status"
  exit $status
fi


# Compile messages. build `django.po` file, it will ignore in the code base
#python manage.py compilemessages -l fa
#status=$?
#if [ $status -ne 0 ]; then
#  echo "Failed to compilemessages: $status"
#  exit $status
#fi


# Collect staticfiles to AWS
# This step can't apply in Dockerfile because we don't have access to our
# environment data, and for sure AWS credentials

python manage.py collectstatic --no-input
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to collect staticfiles: $status"
  exit $status
fi


# to find more checkout supercronic which is a crontab-compatible job runner,
# designed specifically to run in containers.
# <https://github.com/aptible/supercronic>

# Configure cron service
#mkdir -p /run/cron
#python /usr/app/deployment/cron.py
#
## Start cron service
#echo "[CRON] Starting...";
#supercronic ${SUPERCRONIC_OPTIONS} /run/cron/crontab &


# We use Gunicorn using WSGI to deploy the django production
# and Nginx as WebServer.

# Let's start Gunicorn
gunicorn nilmal.wsgi:application
