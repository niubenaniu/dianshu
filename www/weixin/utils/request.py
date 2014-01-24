#-*- coding:utf-8 -*-
import pycurl
import StringIO
import logging
import traceback
import urllib

class HttpRequest:
	
	def get(self, url, params={}):
		_ret = ''
		_url = '%s?%s' % (url, urllib.urlencode(params))
		try:
			_io = StringIO.StringIO()
			_curl = pycurl.Curl()
			_curl.setopt(pycurl.URL, _url)
			_curl.setopt(pycurl.WRITEFUNCTION, _io.write)
                        _curl.setopt(pycurl.SSL_VERIFYPEER, 0)
                        _curl.setopt(pycurl.SSL_VERIFYHOST, 0)
			_curl.setopt(pycurl.HEADER, False)
			_curl.perform()
			_ret = _io.getvalue()
			_io.close()
			_curl.close()
			logging.debug('GET URL:%s' % _url)
		except BaseException as e:
			logging.error('GET URL ERROR:%s' % _url)
			logging.exception(traceback.format_exc())
	
		return _ret

	def post(url, params):
		pass


if __name__ == '__main__':
	hr = HttpRequest()
	print hr.get('www.baidu.com')
