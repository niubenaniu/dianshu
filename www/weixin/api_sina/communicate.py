#-*- coding:utf-8 -*-
import logging
import traceback
import os
import sys

_lib_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_lib_home = os.path.normpath(_lib_home)

if not(_lib_home in sys.path):
        sys.path.insert(0, _lib_home)

from utils.request import HttpRequest
from utils import xmljson
from utils import log

class RequestAPI:
    def __init__(self):
        self.hr = HttpRequest()
        self.home = 'http://s.weibo.com/'
        self.url_search_comment = 'wb/%s'
        
    def search_comment(self, keyword, offset=0, sort='hot'):
        _url = '%s/%s' % (self.home, self.url_search_comment % keyword)
        _ret = self.hr.get(_url,
                           {'offset' : offset,
                            'xsort' : sort,
                            'scope' : 'ori',
                            'page' : offset
                           })
        logging.debug('search result:%s' % _ret)

        return _ret

if __name__ == '__main__':
    log.initlog('', True)
    rapi = RequestAPI()

    print rapi.search_comment('百年孤独')
