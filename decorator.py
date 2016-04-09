# -*- coding: utf-8 -*-
# @Author: yuqing5
# date: 20151023
import tushare as ts
import datetime
import time
import os
import cPickle
import functools

def running_time(func):
    import datetime
    import functools
    @functools.wraps(func)
    def wrapper(*args, **kw):
        start_time = datetime.datetime.now()
        ret = func(*args, **kw)
        end_time = datetime.datetime.now()
        print '[%s()] done, run time : %r sec' % (func.__name__, (end_time - start_time).seconds)
        return ret
    return wrapper

'''
需要传参数的装饰器，则需要编写一个返回decorator的decorator
'''
def load_memcached(prefix):
    #1.一阶套
    def decorator(function):
        print 'In decorator'
        @functools.wraps(function)
        def wrapper(*args, **kw):
            print 'In wrapper'
            today = time.strftime("%Y%m%d",time.localtime())
            file_name = prefix + '_' + today
            result = None
            if os.path.exists(file_name):
                print 'load local:{0}'.format(file_name)
                result =  cPickle.load(file(file_name))
            else:
                result = function(*args, **kw)
                cPickle.dump(result, file(file_name,'w'))
                print 'load internet and memcached:{0}'.format(file_name)
            return result
        return wrapper
    return decorator


#这里直接先执行，返回一个传入参数的装饰器
@load_memcached('nanshou')
def get_concept_classified(funcname):
    print 'In get_concept_classified'
    raw_data = funcname()
    print 'after get_concept_classified'
    return raw_data

ll = get_concept_classified(ts.get_concept_classified)
print ll
