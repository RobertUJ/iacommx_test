#!/bin/sh

# exec fastapi with fastapi-cli commands and options

set -xe

if [ "$DEBUG" = "True" ]; then
    exec fastapi dev src/main.py --host 0.0.0.0
else
    exec fastapi run src/main.py --host 0.0.0.0
fi

#
#if [ "$CELERY_WORKER" = "True" ]; then
#
#  # Run in debug mode
#  if [ "$DEBUG" = "True" ]; then
#    exec celery -A src.celery_worker worker --loglevel=debug --pool=solo
#  else
#    exec celery -A src.celery_worker worker --pool=solo --loglevel=info
#  fi
#
#  # Run flower monitoring tool
#  if [ "$CELERY_FLOWER" = "True" ]; then
#    exec celery -A src.celery_worker flower --port=5555
#  fi
#
#fi
