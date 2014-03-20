#-*- coding:utf-8 -*-
import logging
import traceback
import simplejson
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
            self.home = 'https://api.douban.com'
            self.book_home = 'http://book.douban.com'    # 为了获取评价详情，必须在图书信息主页爬取数据  by niuben at 2014-03-20
            self.home_no_ssl = 'http://api.douban.com'
            self.url_search_book = 'v2/book/search'
            self.url_get_book = 'v2/book/%s'
            self.url_get_book_tag = 'v2/book/%s/tags'
            self.url_get_book_review = 'book/subject/%s/reviews'
            self.url_get_book_by_isbn = '/v2/book/isbn/%s'
            self.url_get_ratings = 'subject/%s'    # by niuben at 2014-03-20

	def search_books(self, keyword, tag='', offset=0, limit=1):
		_url = '%s/%s' % (self.home, self.url_search_book)
		_ret = self.hr.get(_url, {'q' : keyword, \
					   'tag' : tag, \
					   'start' : offset, \
					   'count' : limit})
		logging.debug('search book result:%s' % _ret)
		return simplejson.loads(_ret) if _ret else {}

	def get_book(self, id):
		_url = '%s/%s' % (self.home, self.url_get_book % id)
		_ret = self.hr.get(_url)
		logging.debug('get book restult:%s' % _ret)
		return simplejson.loads(_ret) if _ret else {}

	def get_book_tags(self, id):
		_url = '%s/%s' % (self.home, self.url_get_book_tag % id)
		_ret = self.hr.get(_url)
		logging.debug('get book tag result:%s' % _ret)
		return simplejson.loads(_ret) if _ret else {}

	def get_book_reviews(self, id, offset=0, limit=5, orderby_time=False):
		_url = '%s/%s' % (self.home_no_ssl, self.url_get_book_review % id)
        # 默认按投票排序(score)，time表示按发布时间排序
		_orderby = 'time' if orderby_time else 'score'
		_ret = self.hr.get(_url, {'start-index' : offset,\
					  'max-results' : limit,\
					  'orderby' : _orderby})
		logging.debug('get book reviews xml:%s' % _ret)
		_j_ret = xmljson.xml2json(_ret)
		logging.debug('get book reviews:%s' % _j_ret)
		return _j_ret

        #return simplejson.loads(_ret) if _ret else {} 

        def get_book_by_isbn(self, isbn):
                _url = '%s/%s' % (self.home, self.url_get_book_by_isbn % isbn)
		_ret = self.hr.get(_url)
		logging.debug('get book by isbn:%s' % _ret)
		return simplejson.loads(_ret) if _ret else {}
    
        def get_ratings(self,id):
            _url = '%s/%s/' % (self.book_home, self.url_get_ratings % str(id))
            _ret = self.hr.get(_url)
            logging.debug('get book ratings result:%s' % _ret)
            
            import re
            _reg_exp_node = re.compile(r'(<span\s+class=\"stars5.+<span\s+class=\"stars1.+?\<br\>)',re.S)
            _ratings_node_m = _reg_exp_node.search(_ret)
            
            if _ratings_node_m is not None:
                _reg_exp_ratings = re.compile(r'stars5.+?(\S+)%<br>.+stars4.+?(\S+)%<br>.+stars3.+?(\S+)%<br>.+stars2.+?(\S+)%<br>.+stars1.+?(\S+)%<br>',re.S)
                _ratings_m = _reg_exp_ratings.search(_ratings_node_m.group(0))
                
                if _ratings_m is not None:
                    _ratings = []
                    _ratings = [
                                {
                                 'name': '力荐',
                                 'y': float(_ratings_m.group(1))
                                 },
                                {
                                 'name': '推荐',
                                 'y': float(_ratings_m.group(2))
                                 },
                                {
                                 'name': '还行',
                                 'y': float(_ratings_m.group(3))
                                 },
                                {
                                 'name': '较差',
                                 'y': float(_ratings_m.group(4))
                                 },
                                {
                                 'name': '很差',
                                 'y': float(_ratings_m.group(5))
                                 },
                                ]
                    
                    _j_ratings = simplejson.dumps(_ratings)
                    return _j_ratings
                else:
                    return simplejson.dumps({})
                    
            else:
                return simplejson.dumps({})

if __name__ == '__main__':
	import utils.log
	log.initlog('', True)
	rapi = RequestAPI()
#	print rapi.search_books('c')
#	print rapi.get_book(2193877)
#	print rapi.get_book_tags(2193877)
#	print rapi.get_book_reviews(2193877)

	#print rapi.get_book_reviews(2193877, 0, 1, False)
    
        print rapi.get_ratings(6082808)
