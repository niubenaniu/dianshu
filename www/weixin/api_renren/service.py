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

        _res = []
        _root = ET.fromstring('<?xml version="1.0" encoding="utf-8" ?><root>' + _x + '</root>')
        _node = None
        _n = None
        if _root:
            for _n in _root:
                if _n.tag == 'div' and _n.attrib['class'] == 'search_left_third':
                    _node = _n
                    break
                
        if _node:
            for _n in _node:
                if _n.tag == 'div' and _n.attrib['class'] == 'search_log':
                    _node = _n
                    break
                
        if _node:
            for _n in _node:
                _rs = self._parse_comment_node(_n)
                if _rs:
                    _res.append(_rs)

        return _res

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
    
