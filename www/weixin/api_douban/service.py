#-*- coding:utf-8 -*-
import logging
import traceback
import os
import sys

import configs

from communicate import RequestAPI

_lib_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_lib_home = os.path.normpath(_lib_home)

if not(_lib_home in sys.path):
        sys.path.insert(0, _lib_home)

from utils import log
from dbutils import DbFactory
dbfry = DbFactory()

class RequestService:

    def __init__(self):
        self.dbHandler = dbfry.getInterface('mongodb', configs.db)
        self.dbHandler.connect()
        self.requestAPI = RequestAPI()
        self.collection = 'douban_book'
        pass
        
    def search_books(self, keyword, tag='', offset=0, limit=1):
        _res = self.requestAPI.search_books(keyword, tag, offset, limit)
        if _res.has_key('books'):
            self.dbHandler.connect()
            for _book in _res['books']:
                _exist_book = self.dbHandler.find_one(self.collection, {'isbn13' : _book['isbn13']})
                if not _exist_book:
                    self.dbHandler.insert(self.collection, _book)
            self.dbHandler.disconnect()
        return _res
        
    def search_book_by_isbn(self, isbn):
        self.dbHandler.connect()
        _book = self.dbHandler.find_one(self.collection, {'isbn13' : str(isbn)})
        self.dbHandler.disconnect()
        return _book


if __name__ == '__main__':
    log.initlog('', True)
    service = RequestService()
    service.search_books("百年孤独")
    print service.search_book_by_isbn('9787532706907')
    pass

