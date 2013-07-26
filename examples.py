#! /usr/bin/env python
#coding: utf-8

import time
import random
import string
from datetime import datetime

from bst import BinarySearchTree
from treap import Treap
from decorators import profile, profileit, print_stats

@profileit
def generate_data(number = 1000000):
    """Format: 2013-07-14 20:31:45 liuyun"""
    startdate = int(time.mktime(datetime(2013, 5, 1).timetuple()))
    enddate = int(time.mktime(datetime(2013, 8, 31).timetuple()))
    with open('test.dat', 'w') as f:
        for i in xrange(number):
            timestamp = random.randint(startdate, enddate)
            f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)))
            f.write('    ')
            f.write(''.join(random.sample(string.letters, 6)))
            f.write('\n')


def compare():
    d = {}
    t = BinarySearchTree()
    treap = Treap()
    #with open('test.dat', 'r') as f:
    #    for line in f:
    #        timestamp, user = line.rsplit(' ', 1)
    #        d[timestamp] = user
    #        t.put(timestamp, user)
    #        treap.put(timestamp, user)
    tmin = '2013-07-01 12:00:00'
    tmax = '2013-07-05 18:00:00'
    t0 = time.time()
    with open('test.dat', 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            d[timestamp] = user
    t1 = time.time()
    result = [e for e in d if tmin < e < tmax ]
    t2 = time.time()
    print 'Time-consuming(dict) : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))
    
    t0 = time.time()
    with open('test.dat', 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            t.put(timestamp, user)
    t1 = time.time()
    result = t.searchRange(tmin, tmax)
    t2 = time.time()
    print 'Time-consuming(bst)  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))
    
    t0 = time.time()
    with open('test.dat', 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            treap.put(timestamp, user)
    t1 = time.time()
    result = treap.searchRange(tmin, tmax)
    t2 = time.time()
    print 'Time-consuming(treap): [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))



if __name__ == '__main__':
    #generate_data()
    compare()

