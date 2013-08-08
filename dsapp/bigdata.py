#! /usr/bin/env python
# coding: utf-8

import random
import heapq
import string
import time

from pprint import pprint

################################################################################

TDATA = '%s.dat' % __file__

def generate_vast_IP(total = 10000000):
    """
    Generate only 10,000,000 ips to have a test as a demo.
    
    total: 10,000,000
    unique: 3,000,000
    time consuming:  116.20299983
    """
    with open(TDATA, 'w') as f:
        for i in xrange(total):
            b = random.randint(1, 45)
            c = random.randint(0, 256)
            d = random.randint(0, 256)
            f.write('202.%s.%s.%s\n' % (b, c, d))

def generate_words(total = 1000000):
    with open(TDATA, 'w') as f:
        letters = string.letters[:26]
        for i in xrange(total):
            ri = random.randint(2, 12)
            f.write(''.join(random.sample(letters, ri)))
            f.write('\n')

def test_generate():
    t0 = time.time()
    generate_words(1000000)
    print 'time consuming: ', time.time() - t0

################################################################################

def find_max(tempdirs = []):
    """Method: divide-and-conquer + hash stat + sort
    
    con: can not used to find top k, but only find max.
    
    time consuming:  3.95299983025
    [('my', 163),
     ('sq', 164),
     ('mh', 164),
     ('mo', 165),
     ('im', 167),
     ('ux', 168),
     ('br', 169),
     ('gj', 169),
     ('ij', 170),
     ('qd', 171)]
    """
    fd = {}
    result = []
    
    # divide+hash
    with open(TDATA) as f:
        for line in f:
            fi = '%03i' % (hash(line.strip())%100)
            if fi not in fd:
                fd[fi] = open('tmp/%s.dat'%fi, 'w+')
            fd[fi].write(line)

    # hash_stat+sort
    for fi in fd:
        f = fd[fi]
        f.flush()
        f.seek(0)
        md = {}
        for line in f:
            ip = line.strip()
            md[ip] = md.setdefault(ip, 0) + 1
        tmp = sorted(md.iteritems(), key=lambda d: d[1])
        result.append(tmp[-1])
        f.close()
        
    return sorted(result, key=lambda d: d[1])

def test_find_max():
    t0 = time.time()
    res = find_max()
    print 'time consuming: ', time.time() - t0
    pprint(res[-10:])

################################################################################


def find_top_k(k = 10):
    """Method: divide-and-conquer + hash stat + heap
    
    time consuming:  61.2349998951
    (14, '202.40.136.38')
    (14, '202.43.158.225')
    (14, '202.44.77.103')
    (14, '202.45.235.6')
    (14, '202.9.53.21')
    (15, '202.21.31.17')
    (15, '202.34.112.151')
    (15, '202.39.209.255')
    (15, '202.45.250.204')
    (15, '202.6.99.167')
    
    time consuming:  3.8599998951
    (164, 'mh')
    (164, 'sq')
    (165, 'bi')
    (165, 'mo')
    (167, 'im')
    (168, 'ux')
    (169, 'br')
    (169, 'gj')
    (170, 'ij')
    (171, 'qd')
    """
    fd = {}
    result = []
    
    # divide+hash
    with open(TDATA) as f:
        for line in f:
            fi = '%03i' % (hash(line.strip())%100)
            if fi not in fd:
                fd[fi] = open('tmp/%s.dat'%fi, 'w+')
            fd[fi].write(line)

    # heap+sort
    for fi in fd:
        f = fd[fi]
        f.flush()
        f.seek(0)
        md = {}
        for line in f:
            ip = line.strip()
            md[ip] = md.setdefault(ip, 0) + 1
        for keyword, v in md.iteritems():
            if len(result) < k:
                heapq.heappush(result, (v, keyword))
            else:
                heapq.heappushpop(result, (v, keyword))
        f.close()
        
    return result

def test_find_top_k():
    t0 = time.time()
    #res = find_max()
    res = find_top_k()
    print 'time consuming: ', time.time() - t0
    for i in range(10):
        print heapq.heappop(res)

################################################################################

from trie import Trie
import datrie
import pytrie


def find_top_k_with_trie(k = 10):
    """
    Too slow and large memory consuming.
    
    time consuming:  147.656000137
    (164, 'mh')
    (164, 'sq')
    (165, 'bi')
    (165, 'mo')
    (167, 'im')
    (168, 'ux')
    (169, 'br')
    (169, 'gj')
    (170, 'ij')
    (171, 'qd')
    """
    result = []
    t = Trie()
    # trie
    with open(TDATA) as f:
        for line in f:
            t.insert(line.strip())
    
    # heapq
    for n in t.ipreorder(t.root):
        if len(result) < k:
            heapq.heappush(result, n)
        else:
            heapq.heappushpop(result, n)
            
    return result

def test_find_top_k_with_trie():
    t0 = time.time()
    res = find_top_k_with_trie()
    print 'time consuming: ', time.time() - t0
    for i in range(10):
        print heapq.heappop(res)

def find_top_k_with_datrie(k = 10):
    """
    Too slow for inserts.
        
    time consuming:  896.575999975
    (164, u'mh')
    (164, u'sq')
    (165, u'bi')
    (165, u'mo')
    (167, u'im')
    (168, u'ux')
    (169, u'br')
    (169, u'gj')
    (170, u'ij')
    (171, u'qd')
    """
    result = []
    t = datrie.Trie(string.ascii_lowercase)
    with open(TDATA) as f:
        for line in f:
            key = unicode(line.strip())
            t[key] = t.setdefault(key, 0) + 1

    # heapq
    state = datrie.State(t)
    state.walk(u'A')
    it = datrie.Iterator(state)
    while it.next():
        if len(result) < k:
            heapq.heappush(result, (it.data(), it.key()))
        else:
            heapq.heappushpop(result, (it.data(), it.key()))
            
    return result

def test_find_top_k_with_datrie():
    t0 = time.time()
    res = find_top_k_with_datrie()
    print 'time consuming: ', time.time() - t0
    for i in range(10):
        print heapq.heappop(res)


def find_top_k_with_pytrie(k = 10):
    """
    Too slow for inserts.
        
    time consuming:  57.3159999847
    (164, 'mh')
    (164, 'sq')
    (165, 'bi')
    (165, 'mo')
    (167, 'im')
    (168, 'ux')
    (169, 'br')
    (169, 'gj')
    (170, 'ij')
    (171, 'qd')
    """
    result = []
    t = pytrie.SortedStringTrie()
    with open(TDATA) as f:
        for line in f:
            key = line.strip()
            t[key] = t.setdefault(key, 0) + 1

    # heapq
    for e in t.iteritems():
        if len(result) < k:
            heapq.heappush(result, e[::-1])
        else:
            heapq.heappushpop(result, e[::-1])
            
    return result

def test_find_top_k_with_pytrie():
    t0 = time.time()
    res = find_top_k_with_pytrie()
    print 'time consuming: ', time.time() - t0
    for i in range(10):
        print heapq.heappop(res)


################################################################################

def test(*args, **kw):
    pass

if __name__ == '__main__':
    #test_generate()
    #test_find_max()
    #test_find_top_k()
    #test_find_top_k_with_trie()
    #test_find_top_k_with_datrie()
    test_find_top_k_with_pytrie()
