# module to allow for timing functions

from functools import wraps
from time import time

def func_timer(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print ('func:{0} took: {1} sec'.format(f.__name__, te-ts))
        return result
    return wrap
