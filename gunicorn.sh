#!/bin/bash
set -e
LOGFILE=/home/www/findinshop/var/log/live.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=2

USER=www
GROUP=www
ADDRESS=127.0.0.1:8000
cd /home/www/findinshop
source  .venv/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn_django -w $NUM_WORKERS --bind=$ADDRESS \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE

