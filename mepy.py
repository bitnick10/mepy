import sys
import os
import math

def CleanCacheModules():
    filenames = os.listdir("E:\\My\\Github\\mepy")
    for filename in filenames:
        m = os.path.splitext(filename)[0]
        if m in sys.modules:
            print "clean cache module " + m
            del sys.modules[m]