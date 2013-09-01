#! /usr/bin/env python
# coding: utf-8

import random
import time
from heapq import heappush, heappop, heappushpop
from os.path import join, exists

import numpy as np
from scipy import spatial

import pykdtree
from decorators import timethis
from settings import DATA_PATH

TDATA = '%s.dat' % __file__
def get_data_file(filename = TDATA):
    return filename if exists(filename) else join(DATA_PATH, filename)
TDATA = get_data_file()

def generate_data(n = 1000000):
    with open(TDATA, 'w') as f:
        for i in xrange(n):
            x = random.randint(0, 10000)
            y = random.randint(0, 10000)
            f.write('%s    %s\n' % (x, y))

@timethis
def get_data():
    """
    time consuming:   3.59400010109
    memory consuming: 80 MB
    """
    data = []
    
    with open(TDATA) as f:
        for line in f:
            x, y = [int(e) for e in line.split()]
            data.append((x, y))
    
    return data

@timethis
def knn_with_scipy_cKDTree(data, pt, k = 1):
    """
    k = 1
    
     memory consuming: 97 MB
     construct time:  7.8900001049
     search time:     0.0
     time consuming:  7.96900010109
     result: (array([ 1.]), array([785460]))
     
    k = 3
    
     memory consuming: 106 MB
     construct time:  8.03200006485
     search time:     0.0
     time consuming:  8.11000013351
     (array([[ 1.,  1.41421356,  6.]]), array([[785460, 141226, 331317]]))
    """
    #x, y = np.mgrid[0:5, 2:8]
    t0 = time.time()
    tree = spatial.cKDTree(data)
    t1 = time.time()
    print 'construct time: ', t1-t0
    pts = np.array(pt)
    result = tree.query(pts, k)
    print 'search time: ', time.time()-t1
    
    return result

@timethis
def knn_with_scipy_KDTree(data, pt, k = 1):
    """
    k = 1
    
     memory consuming: 186 MB
     construct time:  23.6720001698
     search time:  0.0
     time consuming: 23.9379999638
     result: (array([ 1.]), array([785460]))
     
    k = 3
    
     memory consuming: 195 MB
     construct time:  23.8120000362
     search time:  0.0
     time consuming: 24.0620000362
     (array([[ 1.,  1.41421356,  6.]]), array([[785460, 141226, 331317]]))
    """
    #x, y = np.mgrid[0:5, 2:8]
    t0 = time.time()
    tree = spatial.KDTree(data)
    t1 = time.time()
    print 'construct time: ', t1-t0
    pts = np.array(pt)
    result = tree.query(pts, k)
    print 'search time: ', time.time()-t1
    
    return result

@timethis
def knn_with_pykdtree(data, pt, k = 1):
    """
    k = 1
    
     memory consuming: 263 MB
     construct time: 62.5779998302
     search time:    0.0
     time consuming: 62.5779998302
     result: ((1000, 999), 1.0)
    
    k = 3
    
     memory consuming: 277 MB
     construct time: 59.3589999676
     search time:  0.0
     time consuming: 59.3589999676
     [((1000, 999), 1.0), ((1001, 999), 1.4142135623730951), ((994, 1000), 6.0)]
    """
    t0 = time.time()
    kdt = pykdtree.KDTree(data)
    t1 = time.time()
    print 'construct time:', t1-t0
    result = kdt.nearest(pt, k)
    print 'search time: ', time.time() - t1
    
    return result

@timethis
def knn_with_heap(data, pt, k = 1):
    """
    memory consuming: 81 MB
    time consuming:   2.93799996376
    [((994, 1000), 6.0), ((1000, 999), 1.0), ((1001, 999), 1.4142135623730951)]
    """
    result  =[]
    
    for e in data:
        dist = pykdtree.distance(pt, e)
        if len(result) < k:
            heappush(result, (-dist, e))
        else:
            heappushpop(result, (-dist, e))
    
    return [(e[1], pow(-e[0], 0.5))for e in result]

if __name__ == '__main__':
    #generate_data()
    data = get_data()
    #print knn_with_scipy_cKDTree(data, [[1000, 1000]], 3)
    #print knn_with_scipy_KDTree(data, [[1000, 1000]], 3)
    print knn_with_pykdtree(data, [1000, 1000], 3)
    #print knn_with_heap(data, [1000, 1000], 3)

