#-*- coding:utf-8 -*-
import pymongo
import bson
import logging
import traceback
import time

class MongodbHandler:
    def __init__(self, configs={}):
        self.configs = configs
        self._client = None
        self._conn = None
        self._retry_conn = 1
        pass

    def _get_conn(self, configs={}):
        _conn = None
        _client = None
        host = configs.get('host', '127.0.0.1')
        port = configs.get('port', 27017)
        dbname = configs.get('dbname', 'test')
        
        try:
            _client = pymongo.MongoClient(host, port)
            _conn = _client[dbname]
        except BaseException as e:
            logging.error("Error Connect Mongodb")
            logging.exception(traceback.format_exc())
        finally:
            return [_client, _conn]
    
    def connect(self):
        _i = 0
        while self._client is None:
            self._client, self._conn = self._get_conn(self.configs)

            if self._client is None:
                _i += 1
                if _i == self._retry_conn:
                    break
                time.sleep(2)
            

    def disconnect(self):
        if self._client:
            self._client.disconnect()

    def insert(self, collection_name, documents):
        if self._conn is None:
            return

        if documents:
            self._conn[collection_name].insert(documents)

    def find(self, collection_name, wheres={}, sorts=None, limit=None, offset=None, returns={}):
        if self._conn is None:
            return []

        if returns:
            _cursor = self._conn[collection_name].find(wheres, returns)
        else:
            _cursor = self._conn[collection_name].find(wheres)

        if not(sorts is None):
            _cursor.sort(sorts)

        if not(offset is None):
            _cursor = _cursor.skip(offset)
            
        if not(limit is None):
            _cursor = _cursor.limit(limit)
        _rs = []
        for _r in _cursor:
            _rs.append(_r)
        _cursor.close()
        return _rs

    def find_all(self, collection_name, wheres={}):
        return self.find(collection_name, wheres)

    def find_one(self, collection_name, wheres={}):
        if self._conn is None:
            return None

        return self._conn[collection_name].find_one(wheres)

    def find_by_oid(self, collection_name, oid):
        return self.find_one(collection_name, {'_id' : bson.objectid.ObjectId(oid)})

    def remove_by_oid(self, collection_name, oid):
        return self.remove(collection_name, {'_id' : bson.objectid.ObjectId(oid)})

    def remove(self, collection_name, wheres={}):
        _rs = None
        if self._conn is None:
            return _rs
        
        if wheres:
            _rs = self._conn[collection_name].remove(wheres)
        return _rs

    def clear(self, collection_name):
        return self._conn[collection_name].remove()


APIHandler = MongodbHandler
    
if __name__ == '__main__':
    handler = MongodbHandler()
    handler.connect()
    handler.insert('aaa', [{'name':'wuke'},{'name':'wuke', 'tel' : 'test'}, {'name' : 'silence', 'sex':'m'}])
    print 'find_all' + '*' * 50
    print handler.find_all('aaa')
    print 'remove' + '*' * 50
    print handler.remove('aaa', {'sex' : 'm'})
    print 'find_all' +  '*' * 50
    print handler.find_all('aaa')
    r = handler.find_one('aaa')
    print 'find_once' + '*' * 50
    print r
    print 'find_by_oid' + ' *' * 50
    print handler.find_by_oid('aaa', str(r['_id']))
    print 'remove by oid' + '*' * 50
    print handler.remove_by_oid('aaa', str(r['_id']))
    print 'find_all' + '*' * 50
    print handler.find_all('aaa')
    print 'clear' + '*' * 50
    print handler.clear('aaa')
    print 'find_all' + '*' * 50
    print handler.find_all('aaa')
    handler.disconnect()

    
