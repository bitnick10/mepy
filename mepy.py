import sys
import os

def CleanCacheModules(dir):
    filenames = os.listdir(dir)
    for filename in filenames:
        m = os.path.splitext(filename)[0]
        if m in sys.modules:
            print "clean cache module " + m
            del sys.modules[m]