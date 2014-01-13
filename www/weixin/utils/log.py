#-*- coding:utf-8 -*-
import logging
import os
import time

def initlog(filename='', debug=False):
	logfile = filename if filename else time.strftime('%Y-%m-%d', time.localtime(time.time()))
	logfile += '.debug.log' if debug else '.relase.log'
	logging.basicConfig(filename=logfile,\
			level=logging.DEBUG,\
			filemode='a',\
			format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',\
			datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
	initlog('', True)
	logging.debug('debug')
