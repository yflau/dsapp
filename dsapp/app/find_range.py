#! /usr/bin/env python
#coding: utf-8

import time
import random
import string
from datetime import datetime

from bst import BinarySearchTree
from treap import Treap
from avl import AVLTree

from decorators import profile, profileit, print_stats

TDATA = '%s.dat' % __file__

@profileit
def generate_data(number = 1000000):
    """Format: 2013-07-14 20:31:45 liuyun"""
    startdate = int(time.mktime(datetime(2013, 5, 1).timetuple()))
    enddate = int(time.mktime(datetime(2013, 8, 31).timetuple()))
    with open(TDATA, 'w') as f:
        for i in xrange(number):
            timestamp = random.randint(startdate, enddate)
            f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)))
            f.write('    ')
            f.write(''.join(random.sample(string.letters, 6)))
            f.write('\n')


def compare():
    """
    1000000 items:
    
    Time-consuming(dict) : [setup]3.3130  [search]0.3120 [result]33346
    Time-consuming(bst)  : [setup]76.7970 [search]0.1250 [result]33346
    Time-consuming(treap): [setup]68.8440 [search]0.0780 [result]33346
    Time-consuming(avl)  : [setup]55.0620 [search]0.0940 [result]33346
    """
    d = {}
    t = BinarySearchTree()
    treap = Treap()
    avl = AVLTree()
    
    tmin = '2013-07-01 12:00:00'
    tmax = '2013-07-05 18:00:00'
    
    t0 = time.time()
    with open(TDATA, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            d[timestamp] = user
    t1 = time.time()
    result = [e for e in d if tmin < e < tmax ]
    t2 = time.time()
    print 'Time-consuming(dict) : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))
    
    t0 = time.time()
    with open(TDATA, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            t.put(timestamp, user)
    t1 = time.time()
    result = t.searchRange(tmin, tmax)
    t2 = time.time()
    print 'Time-consuming(bst)  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))
    
    t0 = time.time()
    with open(TDATA, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            treap.put(timestamp, user)
    t1 = time.time()
    result = treap.searchRange(tmin, tmax)
    t2 = time.time()
    print 'Time-consuming(treap): [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))

    t0 = time.time()
    with open(TDATA, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            avl.put(timestamp, user)
    t1 = time.time()
    result = avl.searchRange(tmin, tmax)
    t2 = time.time()
    print 'Time-consuming(avl)  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))


if __name__ == '__main__':
    #generate_data()
    compare()

