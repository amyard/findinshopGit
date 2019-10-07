#!/bin/bash
set -e
LOGFILE=/home/www/findinshop_live/findinshop/var/log/live_celery.log
LOGDIR=$(dirname $LOGFILE)

cd /home/www/findinshop_live/findinshop
source env/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec celery worker -B -A source --loglevel=INFO

