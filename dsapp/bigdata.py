#! /usr/bin/env python
# coding: utf-8

import random
import heapq
import string
import time
from os.path import join, exists

from pprint import pprint

from decorators import timethis
from settings import DATA_PATH

################################################################################

TDATA = '%s.dat' % __file__
def get_data_file(filename = TDATA):
    return filename if exists(filename) else join(DATA_PATH, filename)
TDATA = get_data_file()

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

def generate_words(filename = TDATA, total = 1000000):
    with open(filename, 'w') as f:
        letters = string.letters[:26]
        for i in xrange(total):
            ri = random.randint(2, 12)
            f.write(''.join(random.sample(letters, ri)))
            f.write('\n')

def test_generate():
    t0 = time.time()
    generate_words(TDATA, 1000000)
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
    
    memory consuming: 10 MB
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
import hat_trie

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
        
    memory consuming: 730 MB
    time consuming:  61.0309998989
    (165, 'ts')
    (165, 'um')
    (165, 'yk')
    (165, 'zl')
    (166, 'ky')
    (166, 'sg')
    (167, 'nh')
    (169, 'kp')
    (171, 'eo')
    (172, 'dq')
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

@timethis
def find_top_k_with_hat_trie(filename = TDATA, k = 10):
    """
    Profile result:
      
      1 million strings:
      time consuming: 4.34599995613
      memory consuming: 23 MB
        
      [(165, u'ts'),
       (165, u'yk'),
       (165, u'um'),
       (166, u'ky'),
       (165, u'zl'),
       (166, u'sg'),
       (167, u'nh'),
       (171, u'eo'),
       (172, u'dq'),
       (169, u'kp')]
      
      5 million strings:
      memory consuming: 85 MB
      time consuming: 25.5469999313
      [(753, u'bf'),
       (753, u'qj'),
       (753, u'zb'),
       (753, u'vz'),
       (755, u'lx'),
       (768, u'bg'),
       (767, u'tf'),
       (779, u'qp'),
       (763, u'ma'),
       (758, u'eq')]
    """
    result = []
    t = hat_trie.Trie()
    with open(filename) as f:
        for line in f:
            key = unicode(line.strip())
            t[key] = t.setdefault(key, 0) + 1

    # heapq
    for key in t.iterkeys():
        key = unicode(key)
        if len(result) < k:
            heapq.heappush(result, (t[key], key))
        else:
            heapq.heappushpop(result, (t[key], key))
    
    return result

@timethis
def find_top_k_with_dict(filename = TDATA, k = 10):
    """
    Profile result:
      
      1 million strings:
      memory consuming: 68 MB
      time consuming: 2.81200003624
        
      [(165, u'ts'),
       (165, u'um'),
       (166, u'ky'),
       (165, u'zl'),
       (165, u'yk'),
       (169, u'kp'),
       (166, u'sg'),
       (172, u'dq'),
       (171, u'eo'),
       (167, u'nh')]
       
       5 million strings:
       memory consuming: 236 MB
       time consuming: 15.0160000324
       [(753, u'bf'),
        (753, u'zb'),
        (753, u'qj'),
        (763, u'ma'),
        (755, u'lx'),
        (753, u'vz'),
        (768, u'bg'),
        (779, u'qp'),
        (767, u'tf'),
        (758, u'eq')]
    """
    result = []
    t = {}
    with open(filename) as f:
        for line in f:
            key = line.strip()
            t[key] = t.setdefault(key, 0) + 1

    # heapq
    for key in t.iterkeys():
        key = unicode(key)
        if len(result) < k:
            heapq.heappush(result, (t[key], key))
        else:
            heapq.heappushpop(result, (t[key], key))
    
    return result


from bintrees import FastAVLTree, FastRBTree

@timethis
def find_top_k_with_avltree(filename = TDATA, k = 10):
    """
    Profile result:
       
       5 million strings:
       memory consuming: 259 MB
       time consuming: 88.2190001011
       [(753, 'bf'),
        (753, 'qj'),
        (753, 'zb'),
        (753, 'vz'),
        (763, 'ma'),
        (755, 'lx'),
        (779, 'qp'),
        (768, 'bg'),
        (758, 'eq'),
        (767, 'tf')]
    """
    result = []
    t = FastAVLTree()
    with open(filename) as f:
        for line in f:
            key = line.strip()
            t[key] = t.setdefault(key, 0) + 1

    # heapq
    for key, val in t.iter_items():
        if len(result) < k:
            heapq.heappush(result, (val, key))
        else:
            heapq.heappushpop(result, (val, key))
    
    return result

@timethis
def find_top_k_with_FastRBTree(filename = TDATA, k = 10):
    """
    Profile result:
       
       5 million strings:
       memory consuming: 259 MB
       time consuming: 39.9689998627
       [(753, 'bf'),
        (753, 'qj'),
        (753, 'zb'),
        (753, 'vz'),
        (763, 'ma'),
        (755, 'lx'),
        (779, 'qp'),
        (768, 'bg'),
        (758, 'eq'),
        (767, 'tf')]
    """
    result = []
    t = FastRBTree()
    with open(filename) as f:
        for line in f:
            key = line.strip()
            t[key] = t.setdefault(key, 0) + 1

    # heapq
    for key, val in t.iter_items():
        if len(result) < k:
            heapq.heappush(result, (val, key))
        else:
            heapq.heappushpop(result, (val, key))
    
    return result

import rbtree

@timethis
def find_top_k_with_rbtree(filename = TDATA, k = 10):
    """
    Profile result:
       
       5 million strings:
       memory consuming: 259 MB
       time consuming: 92.625
       [(753, 'bf'),
        (753, 'qj'),
        (753, 'zb'),
        (753, 'vz'),
        (763, 'ma'),
        (755, 'lx'),
        (779, 'qp'),
        (768, 'bg'),
        (758, 'eq'),
        (767, 'tf')]
    """
    result = []
    t = rbtree.rbtree()
    with open(filename) as f:
        for line in f:
            key = line.strip()
            t[key] = t.setdefault(key, 0) + 1

    # heapq
    for key, val in t.iteritems():
        if len(result) < k:
            heapq.heappush(result, (val, key))
        else:
            heapq.heappushpop(res<input type="image" src="">ult, (val, key))
    
    return result

################################################################################

@timethis
def find_words_by_prefix_with_hat_trie(filename = TDATA, prefix = 'abcd'):
    """
    Profile result:
    
      1 million strings:
      memory consuming: 23 MB
      time consuming: 3.5150001049
      [u'', u'kxqjveg', u'ts']
      
      5 million strings:
      memory consuming: 85 MB
      search time: 0.0
      time consuming: 19.5780000687
      [u'',
       u'fqxe',
       u'xj',
       u'ihlrygtx',
       u'iuhxe',
       u'hwtl',
       u'pfjxywg',
       u'gpnk',
       u'igrh',
       u'xwpji',
       u'qvmujhfp']
    """
    t = hat_trie.Trie()
    with open(filename) as f:
        for line in f:
            key = unicode(line.strip())
            t[key] = t.setdefault(key, 0) + 1
    
    t0 = time.time()
    result = t.keys_with_prefix(prefix)
    print 'search time: %s' % (time.time() - t0)
    
    return result

@timethis
def find_words_by_prefix_with_dict(filename = TDATA, prefix = 'abcd'):
    """
    Profile result:
      
      1 million strings:
      memory consuming: 70 MB
      time consuming: 2.64100003242
      [u'abcdts', u'abcdkxqjveg', u'abcd']
      
      5 million strings:
      memory consuming: 280 MB
      search time: 2.84299993515
      time consuming: 14.0309998989
      [u'abcdigrh',
       u'abcdhwtl',
       u'abcdiuhxe',
       u'abcdxj',
       u'abcdqvmujhfp',
       u'abcdpfjxywg',
       u'abcdgpnk',
       u'abcdxwpji',
       u'abcdihlrygtx',
       u'abcd',
       u'abcdfqxe']
    """
    result = []
    t = {}
    with open(filename) as f:
        for line in f:
            key = unicode(line.strip())
            t[key] = t.setdefault(key, 0) + 1
    
    t0 = time.time()
    for key in t:
        if key.startswith(prefix):
            result.append(key)
    print 'search time: %s' % (time.time() - t0)
    
    return result

################################################################################

def test(*args, **kw):
    pass

if __name__ == '__main__':
    #test_generate()
    #test_find_max()
    #test_find_top_k()
    #test_find_top_k_with_trie()
    #test_find_top_k_with_datrie()
    #test_find_top_k_with_pytrie()
    #pprint(find_top_k_with_hat_trie())
    #pprint(find_top_k_with_dict())
    
    #generate_words('5ms.dat', 5000000)
    #pprint(find_top_k_with_hat_trie(get_data_file('5ms.dat')))
    #pprint(find_top_k_with_dict(get_data_file('5ms.dat')))
    #pprint(find_top_k_with_avltree(get_data_file('5ms.dat')))
    #pprint(find_top_k_with_FastRBTree(get_data_file('5ms.dat')))
    pprint(find_top_k_with_rbtree(get_data_file('5ms.dat')))
    
    #pprint(find_words_by_prefix_with_hat_trie(get_data_file('5ms.dat')))
    #pprint(find_words_by_prefix_with_dict(get_data_file('5ms.dat')))
