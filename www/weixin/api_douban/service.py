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
        self.requestAPI = RequestAPI()
        self.collection = 'douban_book'
        pass
        
    def search_books(self, keyword, tag='', offset=0, limit=1):
        _res = self.requestAPI.search_books(keyword, tag, offset, limit)
        if _res.has_key('books'):
            try:
                self.dbHandler.connect()
                for _book in _res['books']:
                    self.dbHandler.insert(self.collection, _book)
            except BaseException as e:
                logging.error('error save search books')
                logging.exception(traceback.format_exc())
            finally:
                self.dbHandler.disconnect()
        return _res
        
    def search_book_by_isbn(self, isbn):
        _book = None
        try:
            self.dbHandler.connect()
            _book = self.dbHandler.find_one(self.collection, {'isbn13' : str(isbn)})
        except BaseException as e:
            logging.error('error search book by isbn')
            logging.exception(traceback.format_exc())

        finally:
            self.dbHandler.disconnect()

        if _book is None:
            _book = self.requestAPI.get_book_by_isbn(str(isbn))  # ('9787532706907')
            
        return _book

    def get_book_reviews(self,id, offset=0, limit=5, orderby_time=False):
        _reviews = None
        _reviews = self.requestAPI.get_book_reviews(id, offset=offset, limit=limit, orderby_time=orderby_time)
        
        if _reviews is None:
            return {}
        return _reviews
        
    def get_ratings(self,id):
        _ratings = self.requestAPI.get_ratings(id)
        
        return _ratings
        
if __name__ == '__main__':
    log.initlog('', True)
    service = RequestService()
    service.search_books("百年孤独")
    #print service.search_book_by_isbn('9787532706907')
    #pass
    print service.get_ratings(6082808)
    pass