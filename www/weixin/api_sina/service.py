#-*- coding:utf-8 -*-
import logging
import traceback
import os
import sys
import re
from xml.etree import ElementTree as ET
import simplejson

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
#        _regex = 'STK && STK.pageletM && STK.pageletM.view\({([^}]+)}\)'
        _regex = 'STK && STK.pageletM && STK.pageletM.view\({"pid":"pl_wb_feedlist",.*?"html":([^}]+)}\)'
#        _node_regex = '<dl[^>]+>.*?<dt[^>]+>.*?<a[^>]+>.*?<img.*?src=\\\\"([^"]+)"[^>]+>.*?<\\\\/a>.*?<\\\\/dt>.*?<dd[^>]+>.*?<p[^>]+>(.*?)<\\\\/p>.*?<ul[^>]+>.*?<\\\\/ul>.*?<dl[^>]+>.*?<\\\\/dl>.*?<p[^>]+>.*?<span>(.*?)<\\\\/span>.*?<a[^>]+>(.*?)<\\\\/a>.*?<a[^>]+>(.*?)<\\\\/a>'
        _node_regex = '<dl[^>]+>.*?<dt[^>]+>.*?<a[^>]+>.*?<img.*?src=\\\\"([^"]+)"[^>]+>.*?<\\\\/a>.*?<\\\\/dt>.*?<dd[^>]+>.*?<p[^>]+>.*?<a[^>]+>(.*?)<a[^>]+>.*?<\\\\/a>.*?<\\\\/a>.*?<em>(.*?)<\\\\/em>.*?<\\\\/p>.*?<ul[^>]+>.*?<\\\\/ul>.*?<dl[^>]+>.*?<\\\\/dl>.*?<p[^>]+>.*?<span>(.*?)<\\\\/span>.*?<a[^>]+>(.*?)<\\\\/a>.*?<a[^>]+>(.*?)<\\\\/a>'
        _num_regex = '<a[^>]+>.*?<em[^>]+>.*<\\\\/em>(.*?)</a>.*<a[^>]>(.*?)<\\\\/a>.*?<a[^>]>(.*?)<\\\\/a>'
        _num_map = {1 : 'zan', 2 : 'zhan', 4 : 'ping'}
        _ret = []
        
        for _node in re.findall(_regex, _x):
            for _nd in re.findall(_node_regex, _node):
                _temp = {}
                _temp['img'] = _nd[0]
                _temp['user'] = _nd[1]
                _temp['comment'] = _nd[2]
                _temp['num'] = {}
                _idx = 0
                for _num in re.findall(_num_regex, _nd[3]):
                    _idx += 1
                    _t = _num_map.get(_idx)
                    if _t is not None:
                        _temp['num'][_t] = _num
                _temp['time'] = _nd[4]
                _temp['from'] = _nd[5]
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
    
