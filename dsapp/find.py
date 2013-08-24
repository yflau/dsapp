#! /usr/bin/env python
#coding: utf-8

import time
import random
import string
from datetime import datetime
from os.path import join, exists

import rbtree
from bintrees import AVLTree, RBTree, FastAVLTree, FastRBTree
from blist import sorteddict
import sqlite3
from mx.BeeBase import BeeDict
from btree import BPlusTree
from BTrees.OOBTree import OOBTree
from pybtree import BTree

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
        f.write('2013-07-01 12:00:00    liuyun\n')
        f.write('2013-07-05 18:00:00    liufei\n')

def find_range_with_dict(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    ds: Hash table.
    
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

def find_range_with_sorteddict(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    ds: B+Tree
    
    Profile result:
    
      Memory-consuming: 114 MB
      Time-consuming(iter)      : [setup]84.6870 [search]2.3590 [result]32976
      Time-consuming(viewkeys)  : [setup]89.6560 [search]0.0000 [result]32976
    """
    dic = sorteddict()
    
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit('    ', 1)
            dic[timestamp] = user

    t1 = time.time()
    vks = dic.viewkeys()
    imin = vks.index(tmin)
    imax = vks.index(tmax)
    result = vks[imin:imax]
    t2 = time.time()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))

def find_range_with_rbtree(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    ds: RBTree
    
    Profile result:
    
      Memory-consuming: 113 MB
      Time-consuming(iter)  : [setup]4.4690 [search]0.8280 [result]32976
      Time-consuming(slice) : [setup]4.6090 [search]0.0780 [result]32976
    """
    t = rbtree.rbtree()
    
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit('    ', 1)
            t[timestamp] = user
            
    t1 = time.time()
    #result = [e for e in rbt if tmin < e < tmax ]
    result = list(t[tmin:tmax])
    t2 = time.time()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))

def find_range_with_FastAVLTree(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    ds: AVLTree
    
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


def find_range_with_sqlite3(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    Profile result:
    
      Memory-consuming: 82 MB
      Time-consuming(UNIQUE) : [setup]22.0310 [search]0.0630 [result]32976

      Memory-consuming: 51 MB
      Time-consuming         : [setup]12.0780 [search]0.4690 [result]34584
        
      Actually 34584 is the correct solution!!!
    """
    t0 = time.time()
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.executescript("""
        create table log(
            rid INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp char(19) NOT NULL UNIQUE,
            user char(6))""")
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit('    ', 1)
            try:
                cur.execute("insert into log(timestamp,user) values(?,?)", (timestamp, user))
            except:
                pass

    t1 = time.time()
    cur.execute("select timestamp from log where timestamp >= '%s' and timestamp < '%s'" % (tmin, tmax))
    result = cur.fetchall()
    t2 = time.time()
    cur.close()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))


def find_range_with_btree(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    Profile result:
    
    +----------+-----------+-----------+------------+------------+
    |  order   |   setup   |  search   |   result   | memory(MB) |
    +----------+-----------+-----------+------------+------------+
    |    3     |  57.1720  |  1.3910   |   34584    |     188    |
    +----------+-----------+-----------+------------+------------+
    |    4     |  47.6090  |  1.2500   |   34584    |     157    |
    +----------+-----------+-----------+------------+------------+
    |    5     |  41.2650  |  1.0780   |   34584    |     143    |
    +----------+-----------+-----------+------------+------------+
    |    6     |  36.5310  |  1.0160   |   34584    |     134    |
    +----------+-----------+-----------+------------+------------+
    |    7     |  35.1880  |  1.0310   |   34584    |     127    |
    +----------+-----------+-----------+------------+------------+
    |    8     |  32.2660  |  0.9370   |   34584    |     124    |
    +----------+-----------+-----------+------------+------------+
    |    9     |  31.7660  |  0.9220   |   34584    |     122    |
    +----------+-----------+-----------+------------+------------+
    |    10    |  30.9060  |  0.9220   |   34584    |     119    |
    +----------+-----------+-----------+------------+------------+
    |    11    |  29.3750  |  0.8430   |   34584    |     114    |
    +----------+-----------+-----------+------------+------------+
    |    12    |  29.1720  |  0.8280   |   34584    |     112    |
    +----------+-----------+-----------+------------+------------+
    |    13    |  29.0160  |  0.9060   |   34584    |     110    |
    +----------+-----------+-----------+------------+------------+
    |    14    |  28.1880  |  0.8750   |   34584    |     112    |
    +----------+-----------+-----------+------------+------------+
    |    15    |  26.8120  |  0.8280   |   34584    |     111    |
    +----------+-----------+-----------+------------+------------+
    |    16    |  26.5460  |  0.8600   |   34584    |     109    |
    +----------+-----------+-----------+------------+------------+
    |    50    |  22.6560  |  0.7340   |   34584    |     97     |
    +----------+-----------+-----------+------------+------------+
    |    100   |  21.5000  |  0.7030   |   34584    |     98     |
    +----------+-----------+-----------+------------+------------+
    |    500   |  21.7810  |  0.7040   |   34584    |     97     |
    +----------+-----------+-----------+------------+------------+
    |    1000  |  22.4850  |  0.6870   |   34584    |     97     |
    +----------+-----------+-----------+------------+------------+
    """
    d = BPlusTree(1000)
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit('    ', 1)
            d[timestamp] = user

    t1 = time.time()
    keys = d.keys()
    print time.time() - t1
    imin = keys.index(tmin)
    imax = keys.index(tmax)
    result = keys[imin:imax]
    t2 = time.time()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))


def find_range_with_BTrees(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    ds: B+Tree
    
    Profile result:
    
      Memory-consuming: 98 MB
      Time-consuming  : [setup]9.7660 [search]0.0000 [result]32977
    """
    dic = OOBTree()
    
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit('    ', 1)
            dic[timestamp] = user

    t1 = time.time()
    result = dic.keys(tmin, tmax)
    t2 = time.time()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))

def find_range_with_pybtree(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    ds: B-Tree
    
    Profile result:
    
     degree: 500

      Memory-consuming: 92 MB
      Time-consuming  : [setup]15.7970 [search]0.0000 [result]34584
      
      Memory-consuming: 100 MB
      Time-consuming  : [setup]20.4690 [search]0.0000 [result]34584
        
     degree: 1000
      
      Memory-consuming: 93 MB
      Time-consuming(list)  : [setup]16.4530 [search]0.0000 [result]34584
    """
    dic = BTree(500)
    
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit('    ', 1)
            dic[timestamp] = user

    t1 = time.time()
    result = dic.keys(tmin, tmax)
    t2 = time.time()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))

def find_range_with_mxBeeBase(filename = TDATA, tmin = TMIN, tmax = TMAX):
    """
    Faild.
    
    Profile result:
    
      Memory-consuming: 185 MB
      Time-consuming  :
    """
    d = BeeDict.BeeStringDict('tmp/find.py', keysize=100)
    t0 = time.time()
    with open(filename, 'r') as f:
        for line in f:
            timestamp, user = line.rsplit('    ', 1)
            d[timestamp] = user
    d.commit()

    t1 = time.time()
    keys = d.keys()
    imin = keys.index(tmin)
    imax = keys.index(tmax)
    result = keys[imin:imax]
    t2 = time.time()
    d.close()
    print 'Time-consuming  : [setup]%6.4f [search]%6.4f [result]%s' %(t1 - t0, t2 - t1, len(result))


if __name__ == '__main__':
    #generate_data()
    #compare()
    #find_range_with_dict()
    #find_range_with_sorteddict()
    #find_range_with_rbtree()
    #find_range_with_bst()
    #find_range_with_treap()
    #find_range_with_avl()
    #find_range_with_sbt()
    #find_range_with_FastAVLTree()
    #find_range_with_FastRBTree()
    #find_range_with_sqlite3()
    #find_range_with_btree()
    #find_range_with_BTrees()
    find_range_with_pybtree()
    #find_range_with_mxBeeBase()

