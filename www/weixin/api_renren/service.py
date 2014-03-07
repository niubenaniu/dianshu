#-*- coding:utf-8 -*-
import logging
import traceback
import os
import sys
import re
from xml.etree import ElementTree as ET

_lib_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_lib_home = os.path.normpath(_lib_home)

if not(_lib_home in sys.path):
    sys.path.insert(0, _lib_home)

from utils import log
from dbutils import DbFactory

from communicate import RequestAPI

class RequestService:
    
    def __init__(self):
        self.requestAPI = RequestAPI()
        pass
        
    def search_comment(self, keyword):

        _x = self.requestAPI.search_comment(keyword)
        _regex = '<div class="all_list_node">\s+<div[^>]+>\s+<a[^>]+>\s+<img([^>]+)>\s+</a>\s+</div>\s+<div[^>]+>\s+<div[^>]+>\s+<a[^>]+>([^<]+)</a><span[^<]+</span>\s+<div[^>]+>(.*?)</div>\s+</div>\s+<div[^>]+>\s+<font[^>]+>([^<]+)</font>\s+<span[^>]+>(.*?)</span>\s+</div>'
        _regex = '<div class="all_list_node">\s+<div[^>]+>\s+<a[^>]+>\s+<img.*?data-src="([^"]+)"[^>]+>\s+</a>\s+</div>\s+<div[^>]+>\s+<div[^>]+>\s+<a[^>]+>([^<]+)</a><span[^<]+</span>\s+<div[^>]+>(.*?)</div>\s+</div>\s+<div[^>]+>\s+<font[^>]+>([^<]+)</font>\s+<span[^>]+>(.*?)</span>\s+</div>'
        _ret = []
        _content_map = {'img' : 0, 'user' :  1, 'comment' : 2, 'time' : 3, 'num' : 4}
        for _node in re.findall(_regex, _x):
            _temp = {}
            for _i in _content_map:
                _temp[_i] = _node[_content_map[_i]]
            _ret.append(_temp)
        return _ret

    def _parse_comment_node(self, node):
        _rs = {}
        for _n in node:
            if _n.attrib['class'] == 'node_head':
                _img = _n.find('a').find('img')
                if _img:
                    _rs['img'] = _img.attrib['data-src']
                pass
            elif _n.attrib['class'] == 'node_content_all':
                pass

        return _rs

if __name__ == '__main__':
    log.initlog('', True)
    rs = RequestService()
    print rs.search_comment('百年孤独')
    
