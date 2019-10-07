#!./env/bin/python
import os, sys, time, shlex, subprocess

PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

sys.path.insert(0, PROJECT_PATH)

PID_FILE = os.path.join(PROJECT_PATH, 'var/celery.pid')
LOG_FILE = os.path.join(PROJECT_PATH, 'var/log/celery.log')
LOG_LEVEL = 'INFO'
CONCURRENCY = 4

COMMAND = '%s/env/bin/python %s/manage.py celeryd -B start --logfile=%s --loglevel=%s --concurrency=%s' % \
        (PROJECT_PATH, PROJECT_PATH, LOG_FILE, LOG_LEVEL, CONCURRENCY)

def start():
    p = subprocess.Popen(shlex.split(COMMAND), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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


