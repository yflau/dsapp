#! /usr/bin/env python
#coding: utf-8

import time
import random
import string
from datetime import datetime
from os.path import join, exists

import rbtree
from bintrees import AVLTree, RBTree, FastAVLTree, FastRBTree

from bst import BinarySearchTree
from treap import Treap
from avl import AVLTree
from sbt import SBTree

from decorators import timethis
from settings import DATA_PATH

TDATA = '%s.dat' % __file__
def get_data_file(filename = TDATA):
    return filename if exists(filename) else join(DATA_PATH, filename)
TDATA = get_data_file()

TMIN = '2013-07-01 12:00:00'
TMAX = '2013-07-05 18:00:00'

def generate_data(filename = TDATA, number = 1000000):
    """Format: 2013-07-14 20:31:45 liuyun"""
    startdate = int(time.mktime(datetime(2013, 5, 1).timetuple()))
    enddate = int(time.mktime(datetime(2013, 8, 31).timetuple()))
    with open(filename, 'w') as f:
        for i in xrange(number):
            timestamp = random.randint(startdate, enddate)
            f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)))
            f.write('    ')
            f.write(''.join(random.sample(string.letters, 6)))
            f.write('\n')
        f.write('2013-07-01 12:00:00      liuyun\n')
        f.write('2013-07-05 18:00:00      liufei\n')

def find_range_with_dict(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    Profile result:
    
      Memory-consuming: 107 MB
      Time-consuming  : [setup]1.6410 [search]0.3750 [result]32976
    """
    dic = {}
    
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            dic[timestamp] = user
            
    t1 = time.time()
    result = [e for e in dic if tmin < e < tmax ]
    t2 = time.time()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))

def find_range_with_rbtree(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    Profile result:
    
      Memory-consuming: 113 MB
      Time-consuming(iter)  : [setup]4.4690 [search]0.8280 [result]32976
      Time-consuming(slice) : [setup]4.6090 [search]0.0780 [result]32976
    """
    t = rbtree.rbtree()
    
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            t[timestamp] = user
            
    t1 = time.time()
    #result = [e for e in rbt if tmin < e < tmax ]
    result = list(t[tmin:tmax])
    t2 = time.time()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))

def find_range_with_FastAVLTree(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    Profile result:
    
      Memory-consuming: 113 MB
      Time-consuming(TreeSlice) : [setup]8.5320 [search]0.5930 [result]32976
      Time-consuming(succ_key)  : [setup]7.5160 [search]0.2030 [result]32976
    """
    result = []
    t = FastAVLTree()
    
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            t.insert(timestamp, user)
            
    t1 = time.time()
    #result = list(t[tmin:tmax])
    ck = t.ceiling_key(tmin)
    while ck < tmax:
        result.append(ck)
        ck = t.succ_key(ck)
    t2 = time.time()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))

def find_range_with_FastRBTree(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    Profile result:
    
      Memory-consuming: 113 MB
      Time-consuming(TreeSlice) : [setup]7.9690 [search]0.5150 [result]32976
      Time-consuming(key_slice) : [setup]7.7180 [search]0.4690 [result]32976
      Time-consuming(succ_key)  : [setup]7.6410 [search]0.1870 [result]32976
    """
    result = []
    t = FastRBTree()
    
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            t.insert(timestamp, user)
            
    t1 = time.time()
    #result = list(t[tmin:tmax])             # TreeSlice
    #result = list(t.key_slice(tmin, tmax))  # key_slice
    ck = t.ceiling_key(tmin)
    while ck < tmax:
        result.append(ck)
        ck = t.succ_key(ck)
    t2 = time.time()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))

def find_range_with_bst(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    Profile result:
    
      Memory-consuming: 290 MB
      Time-consuming  : [setup]90.1880 [search]0.1400 [result]32976
    """
    t = BinarySearchTree()
    
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            t.put(timestamp, user)
            
    t1 = time.time()
    result = t.searchRange(tmin, tmax)
    t2 = time.time()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))

def find_range_with_treap(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    Profile result:
    
      Memory-consuming: 670 MB
      Time-consuming  : [setup]91.4850 [search]0.0940 [result]32976
    """
    t = Treap()
    
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            t.put(timestamp, user)
            
    t1 = time.time()
    result = t.searchRange(tmin, tmax)
    t2 = time.time()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))

def find_range_with_avl(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    Profile result:
    
      Memory-consuming: 619 MB
      Time-consuming  : [setup]67.5160 [search]0.0940 [result]32976
    """
    t = AVLTree()
    
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            t.put(timestamp, user)
            
    t1 = time.time()
    result = t.searchRange(tmin, tmax)
    t2 = time.time()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))

def find_range_with_sbt(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    Profile result:
    
      Memory-consuming: 619 MB
      Time-consuming  : [setup]108.1870 [search]0.1100 [result]32976
    """
    t = SBTree()
    
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit(' ', 1)
            t.put(timestamp, user)
            
    t1 = time.time()
    result = t.searchRange(tmin, tmax)
    t2 = time.time()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))

if __name__ == '__main__':
    #generate_data()
    #compare()
    #find_range_with_dict()
    #find_range_with_rbtree()
    #find_range_with_bst()
    #find_range_with_treap()
    #find_range_with_avl()
    #find_range_with_sbt()
    find_range_with_FastAVLTree()
    #find_range_with_FastRBTree()

