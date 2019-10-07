#!/bin/bash

case "$1" in
"start")
python /home/www/findinshop/manage.py runfcgi host=127.0.0.1 port=8000  pidfile=/tmp/mysite.pid errlog=/tmp/mysite.log
;;
"stop")
kill -9 `cat /tmp/mysite.pid`
;;
"restart")
$0 stop
sleep 1
$0 start
;;
*) echo "Usage: ./server.sh {start|stop|restart}";;
esac    

