#-*- coding:utf-8 -*-
from xml.etree import ElementTree as ET
import types

def xml2json(x):
	_xml = ET.fromstring(x)
	return _x2j(_xml)
	pass

def _x2j(x):
	_j = {}
	for _a in x.attrib:
		_j[_a] = x.attrib[_a]
	
	if x.text:
		_j['texts'] = x.text
		
	for _n in x:
		_r = _x2j(_n)
		if _r:
                        _tag = _tag_deal(_n.tag)
			if _tag in _j:
				if not(type(_j[_tag]) is types.ListType):
					_j[_tag] = [_j[_tag]]
				_j[_tag].append(_r)
			else:
				_j[_tag] = _r
	return _j

def _tag_deal(_tag):
        return _tag.split(':')[-1].split('}')[-1]

def json2xml(j):
	_xml = ET.fromstring('<root/>')
	_j2x(_xml, j)
	return ET.tostring(_xml)

def _j2x(x, j):
	for _e in j:
		if _e == 'texts':
			x.text = j[_e]
		elif type(j[_e]) is types.ListType:
			for _el in j[_e]:
				_n = x.makeelement(_e, {})
				_j2x(_n, _el)
				x.insert(0, _n)
			pass
		elif type(j[_e]) is types.DictType:
			_n = x.makeelement(_e, {})
			_j2x(_n, j[_e])
			x.insert(0, _n)
			pass
		else:
			x.set(_e, j[_e])

	
if __name__ == '__main__':
	j = xml2json('<?xml version=\'1.0\' encoding=\'utf-8\' ?><root xmlns="http://www.w3.org/2005/Atom" last=\'5\'><user id=\'1\'><tel vaule=\'123\'></tel><tel>erre</tel></user></root>')
	print j
	print json2xml(j)
