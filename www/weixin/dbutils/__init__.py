#-*- coding:utf-8 -*-

class DbException(BaseException):
    
    def __init__(self, msg):
        BaseException.__init__(self, msg)


class DbFactory:
    def __init__(self):
        self._adapter_module_map = {
            'mongodb' : 'mongodb'
        }
    
    def getInterface(self, adapter, configs={}):
        _interface = None
        _module_name = self._adapter_module_map.get(adapter, None)
        if _module_name is None:
            raise DbException('no adapter:%s' % adapter)
        try:
            _module =  __import__(_module_name, globals())
            _interface = _module.APIHandler(configs)
        except BaseException as e:
            raise DbException('module is not found:%s' % _module_name)
        finally:
            return _interface

if __name__ == '__main__':
    f = DbFactory()
    f.getInterface('mongodb')
