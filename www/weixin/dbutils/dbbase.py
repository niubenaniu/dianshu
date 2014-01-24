#-*- coding:utf-8 -*-
#-* coding:utf-8 -*-
import logging
import traceback
import time

class DBHandler:
    def __init__(self, args={}):
        self._conn = None
        self._cursor = None
        self._conn_params = self._format_conn_params(args)

    def _format_conn_params(self, args):
        _conn_params = ''
        for _key in args:
            _conn_params += ' %s=%s ' % (_key, args[_key])
            
        return _conn_params
        
    def _get_conn(self):
        _conn = None
        try:
            _conn = self.get_module_conn(self._conn_params)
        except BaseException as e:
            logging.error('Error Connect Db')
            logging.exception(traceback.format_exc())
        finally:
            return _conn	

    def _get_cursor(self):
        _cursor = None
        try:
            _cursor = self._conn.cursor()
        except BaseException as e:
            logging.error('Error Create Cursor')
            logging.exception(traceback.format_exc())
        finally:
            return _cursor

    def connect(self):
        while self._conn is None:
            self._conn = self._get_conn()
            if self._conn is None:
                time.sleep(5)
                
        while self._cursor is None:
            self._cursor = self._get_cursor()
            if self._cursor is None:
                time.sleep(5)		


    def disconnect(self):
        self.commit()
        if self._cursor not is None:
            self._cursor.close()
            
        if self._conn not is None:
            self._conn.close()

    def execute(self, sql, args=[]):
        try:
            self._cursor.execute(sql, args)
        except BaseException as e:
            logging.error('Error execute')
            logging.exception(traceback.format_exe())
            raise DbException(e)

    def fetchall(self, sql, args=[]):
        _ret = None
        try:
            self._cursor.execute(sql, args)
            _ret = self.cursor.fetchall()
        except BaseException as e:
            logging.error('Error fetch')
            logging.exception(traceback.format_exc())
            raise DbException(e)
        finally:
            return _ret

    def fetchmany(self, sql, num, args=[]):
        _ret = None
        try:
            self._cursor.execute(sql, args)
            _ret = self.cursor.fetchmany(num)
        except BaseException as e:
            logging.error('Error fetch')
            logging.excpetion(traceback.format_exc())
            raise DbException(e)
        finally:
            return _ret

    def fetchone(self, sql, args=[]):
        _ret = None
        try:
            self._cursor.execute(sql, args)
            _ret = self.cursor.fetchone()
        except BaseException as e:
            logging.error('Error fetch')
            logging.exception(traceback.format_exc())
            raise DbException(e)
        finally:
            return _ret

    def transaction(self):
        pass

    def commit(self):
        if self._cursor not is None:
            self._cursor.commit()

    def rollback(self):
        pass
