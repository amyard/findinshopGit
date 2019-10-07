#!./env/bin/python

import os
import sys
import shlex
import subprocess

PROJECT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_PATH)
from source import settings

PID_FILE = os.path.join(PROJECT_PATH, 'var/fcgi.pid')
COMMAND = '%(PROJECT_PATH)s/env/bin/python %(PROJECT_PATH)s/manage.py runfcgi host=%(HOST)s' \
        ' port=%(PORT)s pidfile=%(PID_FILE)s method=%(METHOD)s protocol=fcgi maxrequests=0' \
        % {'PROJECT_PATH': settings.PROJECT_PATH, 'HOST': settings.HOST, 'PORT': settings.PORT, \
        'PID_FILE': PID_FILE, 'METHOD': settings.METHOD}

def start():
    p = subprocess.Popen(shlex.split(COMMAND), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if not os.path.exists(PID_FILE.rsplit('/', 1)[0]):
        os.makedirs(PID_FILE.rsplit('/', 1)[0])
    pid_file = open(PID_FILE, 'w')
    pid_file.seek(0)
    pid_file.write(str(p.pid))
    pid_file.close()

def stop():
    pid_file = open(PID_FILE, 'r')
    pid = pid_file.read()
    pid_file.close()
    pid = pid.strip()
    subprocess.call(['kill', '-s', 'TERM', pid])
    os.remove(PID_FILE)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            start()
        elif 'stop' == sys.argv[1]:
            stop()
        elif 'restart' == sys.argv[1]:
            stop()
            start()
        else:
            print ("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print ("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
