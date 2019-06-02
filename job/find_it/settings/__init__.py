from .production import *
try:
    from .local import *
except:
    print('local.py does not exsists')
    pass
