#!/usr/bin/python

import os
import time

django_process = os.popen('ps -ef | grep -v grep | grep runserver').readlines()
run_cmd = r'/usr/bin/python /root/code/dianshu/www/manage.py runserver 0:80'

while (True):
    django_process = os.popen('ps -ef | grep -v grep | grep runserver').readlines()
    if not django_process:
        os.popen(run_cmd)
    time.sleep(5)
